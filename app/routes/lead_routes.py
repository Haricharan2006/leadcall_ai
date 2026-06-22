from fastapi import APIRouter, HTTPException
from datetime import datetime
from uuid import uuid4

from app.database.mongodb import leads_collection, companies_collection
from app.schemas.lead_schema import LeadCreate

router = APIRouter(prefix="/api/leads", tags=["Leads"])


def clean_doc(doc):
    if doc is None:
        return None

    if "_id" in doc:
        doc["_id"] = str(doc["_id"])

    return doc


@router.get("/{company_id}")
def get_leads(company_id: str, status: str | None = None):
    query = {"company_id": company_id}

    if status:
        query["status"] = status

    leads = list(leads_collection.find(query))
    return [clean_doc(lead) for lead in leads]


@router.post("")
def add_lead(lead: LeadCreate):
    company = companies_collection.find_one({"company_id": lead.company_id})

    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")

    now = datetime.utcnow().isoformat()

    new_lead = {
        "lead_id": "lead_" + str(uuid4())[:8],
        "company_id": lead.company_id,
        "name": lead.name,
        "phone": lead.phone,
        "status": "PENDING",
        "interest_type": None,
        "budget": None,
        "location": None,
        "timeline": None,
        "last_call_id": None,
        "last_campaign_id": None,
        "attempt_count": 0,
        "created_at": now,
        "updated_at": now
    }

    insert_result = leads_collection.insert_one(new_lead)

    new_lead["_id"] = str(insert_result.inserted_id)

    return {
        "message": "Lead added successfully",
        "lead": new_lead
    }


@router.patch("/{lead_id}/reset")
def reset_lead(lead_id: str):
    result = leads_collection.update_one(
        {"lead_id": lead_id},
        {
            "$set": {
                "status": "PENDING",
                "interest_type": None,
                "budget": None,
                "location": None,
                "timeline": None,
                "last_call_id": None,
                "last_campaign_id": None,
                "updated_at": datetime.utcnow().isoformat()
            }
        }
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Lead not found")

    return {"message": "Lead reset to PENDING"}