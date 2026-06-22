from datetime import datetime
from uuid import uuid4
from bson import ObjectId

from app.database.mongodb import leads_collection, companies_collection


def convert_objectid(data):
    if isinstance(data, list):
        return [convert_objectid(item) for item in data]

    if isinstance(data, dict):
        return {
            key: str(value) if isinstance(value, ObjectId) else convert_objectid(value)
            for key, value in data.items()
        }

    return data


def get_leads_by_company(company_id: str, status: str | None = None):
    query = {"company_id": company_id}

    if status:
        query["status"] = status

    leads = list(leads_collection.find(query))
    return convert_objectid(leads)


def create_lead(company_id: str, name: str, phone: str):
    company = companies_collection.find_one({"company_id": company_id})

    if not company:
        return None

    now = datetime.utcnow().isoformat()

    lead = {
        "lead_id": "lead_" + str(uuid4())[:8],
        "company_id": company_id,
        "name": name,
        "phone": phone,
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

    result = leads_collection.insert_one(lead)
    lead["_id"] = result.inserted_id

    return convert_objectid(lead)


def reset_lead_status(lead_id: str):
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
                "failure_reason": None,
                "updated_at": datetime.utcnow().isoformat()
            }
        }
    )

    return result.matched_count > 0