from fastapi import APIRouter, HTTPException, Request
from datetime import datetime
from uuid import uuid4
from bson import ObjectId

from app.core.config import settings
from app.database.mongodb import (
    companies_collection,
    leads_collection,
    campaigns_collection
)
from app.services.vapi_service import start_outbound_call
from app.agent.graph import lead_evaluation_graph

router = APIRouter(prefix="/api/campaigns", tags=["Campaigns"])


def convert_objectid(data):
    if isinstance(data, list):
        return [convert_objectid(item) for item in data]

    if isinstance(data, dict):
        new_data = {}
        for key, value in data.items():
            if isinstance(value, ObjectId):
                new_data[key] = str(value)
            else:
                new_data[key] = convert_objectid(value)
        return new_data

    return data


def is_demo_mode():
    return str(settings.DEMO_MODE).lower() == "true"


def build_demo_transcript(company, lead):
    name = lead.get("name", "").lower()
    company_id = lead.get("company_id", "")

    if "ravi" in name:
        return (
            f"Hello, this is {lead.get('name')}. "
            "I am interested in buying a house. "
            "My budget is 50 lakhs. "
            "I prefer Vijayawada location. "
            "I want to buy within 3 months."
        )

    elif "kiran" in name:
        return (
            f"Hello, this is {lead.get('name')}. "
            "I am busy right now. Please call later in the evening."
        )

    elif "hari" in name or "haricharan" in name:
        return (
            f"Hello, this is {lead.get('name')}. "
            "I am not interested in buying property now. Thank you."
        )

    elif "sita" in name:
        return (
            f"Hello, this is {lead.get('name')}. "
            "I am interested in renting an apartment. "
            "My monthly budget is 15000 rupees. "
            "I prefer Guntur location. "
            "I want to move in next month."
        )

    elif "arjun" in name:
        return (
            f"Hello, this is {lead.get('name')}. "
            "I am busy now. Please call later tomorrow morning."
        )

    elif "manikanta" in name:
        return (
            f"Hello, this is {lead.get('name')}. "
            "I need more details. I cannot decide now."
        )

    else:
        return (
            f"Hello, this is {lead.get('name')}. "
            "I am not interested at this time. Thank you."
        )


@router.post("/start/{company_id}")
def start_campaign(company_id: str, request: Request):
    company = companies_collection.find_one(
        {"company_id": company_id},
        {"_id": 0}
    )

    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    pending_leads = list(leads_collection.find(
        {
            "company_id": company_id,
            "status": "PENDING"
        },
        {"_id": 0}
    ))

    if len(pending_leads) == 0:
        return {
            "message": "No pending leads found",
            "company_id": company_id,
            "demo_mode": is_demo_mode(),
            "total_pending_leads": 0,
            "results": []
        }

    campaign_id = "camp_" + str(uuid4())[:8]
    now = datetime.utcnow().isoformat()

    campaigns_collection.insert_one({
        "campaign_id": campaign_id,
        "company_id": company_id,
        "status": "RUNNING",
        "mode": "DEMO" if is_demo_mode() else "VAPI",
        "total_leads": len(pending_leads),
        "calls_started": 0,
        "calls_failed": 0,
        "created_at": now,
        "updated_at": now
    })

    base_url = str(request.base_url).rstrip("/")
    webhook_url = f"{base_url}/api/webhooks/vapi"

    results = []
    calls_started = 0
    calls_failed = 0

    for lead in pending_leads:
        try:
            if is_demo_mode():
                demo_transcript = build_demo_transcript(company, lead)

                result = lead_evaluation_graph.invoke({
                    "lead_id": lead["lead_id"],
                    "company_id": company_id,
                    "transcript": demo_transcript
                })

                leads_collection.update_one(
                    {
                        "lead_id": lead["lead_id"],
                        "company_id": company_id
                    },
                    {
                        "$set": {
                            "last_campaign_id": campaign_id,
                            "updated_at": datetime.utcnow().isoformat()
                        },
                        "$inc": {
                            "attempt_count": 1
                        }
                    }
                )

                calls_started += 1

                results.append({
                    "lead_id": lead["lead_id"],
                    "name": lead["name"],
                    "mode": "DEMO",
                    "status": result.get("status"),
                    "confidence": result.get("confidence"),
                    "message": "Demo transcript processed by LangGraph"
                })

            else:
                vapi_response = start_outbound_call(
                    company=company,
                    lead=lead,
                    webhook_url=webhook_url
                )

                vapi_call_id = vapi_response.get("id")

                leads_collection.update_one(
                    {
                        "lead_id": lead["lead_id"],
                        "company_id": company_id
                    },
                    {
                        "$set": {
                            "status": "CALL_INITIATED",
                            "last_call_id": vapi_call_id,
                            "last_campaign_id": campaign_id,
                            "updated_at": datetime.utcnow().isoformat()
                        },
                        "$inc": {
                            "attempt_count": 1
                        }
                    }
                )

                calls_started += 1

                results.append({
                    "lead_id": lead["lead_id"],
                    "name": lead["name"],
                    "status": "CALL_INITIATED",
                    "vapi_call_id": vapi_call_id
                })

        except Exception as e:
            leads_collection.update_one(
                {
                    "lead_id": lead["lead_id"],
                    "company_id": company_id
                },
                {
                    "$set": {
                        "status": "FAILED",
                        "last_campaign_id": campaign_id,
                        "failure_reason": str(e),
                        "updated_at": datetime.utcnow().isoformat()
                    },
                    "$inc": {
                        "attempt_count": 1
                    }
                }
            )

            calls_failed += 1

            results.append({
                "lead_id": lead["lead_id"],
                "name": lead["name"],
                "status": "FAILED",
                "error": str(e)
            })

    final_status = "COMPLETED" if calls_failed == 0 else "COMPLETED_WITH_ERRORS"

    campaigns_collection.update_one(
        {"campaign_id": campaign_id},
        {
            "$set": {
                "status": final_status,
                "calls_started": calls_started,
                "calls_failed": calls_failed,
                "updated_at": datetime.utcnow().isoformat()
            }
        }
    )

    return {
        "message": "Campaign processed",
        "campaign_id": campaign_id,
        "company_id": company_id,
        "demo_mode": is_demo_mode(),
        "total_leads": len(pending_leads),
        "calls_started": calls_started,
        "calls_failed": calls_failed,
        "webhook_url": webhook_url,
        "results": results
    }


@router.get("/{company_id}")
def get_campaigns(company_id: str):
    campaigns = list(campaigns_collection.find({"company_id": company_id}))
    return convert_objectid(campaigns)
