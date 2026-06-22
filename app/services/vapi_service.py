import requests
from app.core.config import settings

VAPI_CALL_URL = "https://api.vapi.ai/call"


def build_dynamic_vapi_prompt(company, lead):
    questions = company.get("qualification_questions", [])

    questions_text = "\n".join(
        [f"{index + 1}. {question}" for index, question in enumerate(questions)]
    )

    return f"""
You are an advanced AI voice assistant calling on behalf of {company.get("name")}.

Company details:
- Industry: {company.get("industry")}
- Business type: {company.get("business_type")}
- Instructions: {company.get("prompt_instructions")}

Customer details:
- Name: {lead.get("name")}
- Phone: {lead.get("phone")}

Your goal:
Qualify this customer as a real estate lead.

Ask these questions naturally:
{questions_text}

Conversation rules:
- Start with a polite greeting.
- Introduce yourself as an AI assistant calling from {company.get("name")}.
- Ask permission to continue.
- Ask only one question at a time.
- Keep responses short and natural.
- Collect budget, location, and buying/renting timeline.
- If the customer is not interested, politely thank them and end the call.
- If the customer asks to call later, confirm callback preference and end politely.
- Do not pressure the customer.
- Do not claim to be a human.
- Keep the conversation professional.

At the end, summarize the customer's interest clearly.
"""


def validate_vapi_settings():
    if not settings.VAPI_API_KEY or settings.VAPI_API_KEY.startswith("your_"):
        raise Exception("VAPI_API_KEY is missing in backend/.env")

    if not settings.VAPI_ASSISTANT_ID or settings.VAPI_ASSISTANT_ID.startswith("your_"):
        raise Exception("VAPI_ASSISTANT_ID is missing in backend/.env")

    if not settings.VAPI_PHONE_NUMBER_ID or settings.VAPI_PHONE_NUMBER_ID.startswith("your_"):
        raise Exception("VAPI_PHONE_NUMBER_ID is missing in backend/.env")


def start_outbound_call(company, lead, webhook_url):
    validate_vapi_settings()

    dynamic_prompt = build_dynamic_vapi_prompt(company, lead)

    headers = {
        "Authorization": f"Bearer {settings.VAPI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "assistantId": settings.VAPI_ASSISTANT_ID,
        "phoneNumberId": settings.VAPI_PHONE_NUMBER_ID,
        "customer": {
            "number": lead["phone"],
            "name": lead["name"]
        },
        "metadata": {
            "lead_id": lead["lead_id"],
            "company_id": company["company_id"]
        },
        "assistantOverrides": {
            "model": {
                "messages": [
                    {
                        "role": "system",
                        "content": dynamic_prompt
                    }
                ]
            }
        },
        "serverUrl": webhook_url
    }

    response = requests.post(
        VAPI_CALL_URL,
        headers=headers,
        json=payload,
        timeout=30
    )

    if response.status_code not in [200, 201]:
        raise Exception(f"Vapi API error: {response.status_code} - {response.text}")

    return response.json()