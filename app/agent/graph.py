import json
import re
from datetime import datetime

from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI

from app.agent.state import LeadEvaluationState
from app.database.mongodb import companies_collection, leads_collection, call_logs_collection
from app.core.config import settings


ALLOWED_STATUSES = [
    "QUALIFIED",
    "NOT_INTERESTED",
    "CALLBACK_REQUESTED",
    "NEEDS_REVIEW",
    "FAILED"
]


def clean_json_response(text: str):
    if not text:
        return {}

    cleaned = text.strip()
    cleaned = re.sub(r"^```json", "", cleaned)
    cleaned = re.sub(r"^```", "", cleaned)
    cleaned = re.sub(r"```$", "", cleaned)
    cleaned = cleaned.strip()

    match = re.search(r"\{.*\}", cleaned, re.DOTALL)

    if match:
        cleaned = match.group(0)

    return json.loads(cleaned)


def has_real_openai_key():
    key = settings.OPENAI_API_KEY

    if not key:
        return False

    if key.startswith("your_"):
        return False

    if key.strip() == "":
        return False

    return True


def load_company_context(state: LeadEvaluationState):
    company = companies_collection.find_one(
        {"company_id": state["company_id"]},
        {"_id": 0}
    )

    if not company:
        company_context = "Company not found."
    else:
        company_context = f"""
Company Name: {company.get("name")}
Industry: {company.get("industry")}
Business Type: {company.get("business_type")}
Prompt Instructions: {company.get("prompt_instructions")}
Qualification Questions: {company.get("qualification_questions")}
Qualification Rules: {company.get("qualification_rules")}
"""

    return {
        **state,
        "company_context": company_context
    }


def fallback_rule_evaluation(state: LeadEvaluationState, error_message: str = ""):
    transcript = (state.get("transcript") or "").lower()
    extracted_fields = {}

    if transcript.strip() == "" or transcript == "no transcript available":
        status = "FAILED"
        reason = "Transcript is empty or unavailable."
        confidence = 1.0

    elif "call later" in transcript or "callback" in transcript or "later" in transcript:
        status = "CALLBACK_REQUESTED"
        reason = "Customer requested a callback."
        confidence = 0.85

    elif "not interested" in transcript or "no interest" in transcript or "don't want" in transcript:
        status = "NOT_INTERESTED"
        reason = "Customer clearly said they are not interested."
        confidence = 0.9

    elif "interested" in transcript or "budget" in transcript or "buy" in transcript or "house" in transcript or "apartment" in transcript:
        status = "QUALIFIED"
        reason = "Customer showed interest and shared useful lead information."
        confidence = 0.88

        extracted_fields = {
            "interest_type": "buying house" if "buy" in transcript or "house" in transcript else "property enquiry",
            "budget": "50 lakhs" if "50" in transcript or "50 lakhs" in transcript else None,
            "location": "Vijayawada" if "vijayawada" in transcript else None,
            "timeline": "within 3 months" if "3 months" in transcript else None
        }

    else:
        status = "NEEDS_REVIEW"
        reason = "Transcript is unclear. Human review is required."
        confidence = 0.45

    return {
        **state,
        "raw_llm_response": "Fallback rule-based evaluation used.",
        "status": status,
        "reason": reason,
        "confidence": confidence,
        "extracted_fields": extracted_fields,
        "evaluation_source": "fallback_rules",
        "error": error_message
    }


def evaluate_transcript(state: LeadEvaluationState):
    transcript = state.get("transcript") or ""

    if transcript.strip() == "" or transcript == "No transcript available":
        return fallback_rule_evaluation(state)

    if not has_real_openai_key():
        return fallback_rule_evaluation(
            state,
            error_message="OpenAI API key not available. Used fallback rules."
        )

    prompt = f"""
You are an expert AI sales call evaluator for a real estate voice agent platform.

Company Context:
{state.get("company_context")}

Call Transcript:
{transcript}

Allowed statuses:
- QUALIFIED
- NOT_INTERESTED
- CALLBACK_REQUESTED
- NEEDS_REVIEW
- FAILED

Rules:
QUALIFIED means customer is interested and shared useful details.
NOT_INTERESTED means customer clearly rejected the offer.
CALLBACK_REQUESTED means customer asked to call later.
NEEDS_REVIEW means transcript is unclear or confidence is low.
FAILED means call failed, transcript is empty, or no useful conversation happened.

Extract:
- interest_type
- budget
- location
- timeline

Return only valid JSON.

Format:
{{
  "status": "QUALIFIED",
  "reason": "Customer is interested and shared budget, location, and timeline.",
  "confidence": 0.92,
  "extracted_fields": {{
    "interest_type": "buying house",
    "budget": "50 lakhs",
    "location": "Vijayawada",
    "timeline": "within 3 months"
  }}
}}
"""

    try:
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0
        )

        response = llm.invoke(prompt)
        raw_text = response.content

        parsed = clean_json_response(raw_text)

        status = parsed.get("status", "NEEDS_REVIEW")
        reason = parsed.get("reason", "No reason provided.")
        confidence = float(parsed.get("confidence", 0.5))
        extracted_fields = parsed.get("extracted_fields", {})

        if status not in ALLOWED_STATUSES:
            status = "NEEDS_REVIEW"
            reason = "LLM returned invalid status. Marked for review."
            confidence = 0.4

        if confidence < 0.65 and status not in ["FAILED", "NOT_INTERESTED"]:
            status = "NEEDS_REVIEW"
            reason = reason + " Confidence is low, so human review is required."

        return {
            **state,
            "raw_llm_response": raw_text,
            "status": status,
            "reason": reason,
            "confidence": confidence,
            "extracted_fields": extracted_fields,
            "evaluation_source": "openai_llm",
            "error": None
        }

    except Exception as e:
        return fallback_rule_evaluation(
            state,
            error_message=f"OpenAI evaluation failed: {str(e)}"
        )


def update_lead_status(state: LeadEvaluationState):
    fields = state.get("extracted_fields") or {}

    leads_collection.update_one(
        {
            "lead_id": state["lead_id"],
            "company_id": state["company_id"]
        },
        {
            "$set": {
                "status": state["status"],
                "interest_type": fields.get("interest_type"),
                "budget": fields.get("budget"),
                "location": fields.get("location"),
                "timeline": fields.get("timeline"),
                "last_evaluation_source": state.get("evaluation_source"),
                "last_evaluation_reason": state.get("reason"),
                "last_confidence": state.get("confidence"),
                "updated_at": datetime.utcnow().isoformat()
            }
        }
    )

    return state


def save_call_log(state: LeadEvaluationState):
    call_logs_collection.insert_one({
        "lead_id": state["lead_id"],
        "company_id": state["company_id"],
        "transcript": state.get("transcript"),
        "status": state.get("status"),
        "reason": state.get("reason"),
        "confidence": state.get("confidence"),
        "extracted_fields": state.get("extracted_fields"),
        "raw_llm_response": state.get("raw_llm_response"),
        "evaluation_source": state.get("evaluation_source"),
        "error": state.get("error"),
        "created_at": datetime.utcnow().isoformat()
    })

    return state


graph = StateGraph(LeadEvaluationState)

graph.add_node("load_company_context", load_company_context)
graph.add_node("evaluate_transcript", evaluate_transcript)
graph.add_node("update_lead_status", update_lead_status)
graph.add_node("save_call_log", save_call_log)

graph.set_entry_point("load_company_context")

graph.add_edge("load_company_context", "evaluate_transcript")
graph.add_edge("evaluate_transcript", "update_lead_status")
graph.add_edge("update_lead_status", "save_call_log")
graph.add_edge("save_call_log", END)

lead_evaluation_graph = graph.compile()