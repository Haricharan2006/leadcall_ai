from fastapi import APIRouter, HTTPException, Request
from datetime import datetime
from uuid import uuid4
from bson import ObjectId

from app.database.mongodb import (
    companies_collection,
    leads_collection,
    campaigns_collection
)
from app.services.vapi_service import start_outbound_call

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
            "total_pending_leads": 0,
            "results": []
        }

    campaign_id = "camp_" + str(uuid4())[:8]
    now = datetime.utcnow().isoformat()

    campaigns_collection.insert_one({
        "campaign_id": campaign_id,
        "company_id": company_id,
        "status": "RUNNING",
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