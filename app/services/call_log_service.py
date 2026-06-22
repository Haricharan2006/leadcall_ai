from datetime import datetime
from bson import ObjectId
from app.database.mongodb import call_logs_collection


def convert_objectid(data):
    if isinstance(data, list):
        return [convert_objectid(item) for item in data]

    if isinstance(data, dict):
        return {
            key: str(value) if isinstance(value, ObjectId) else convert_objectid(value)
            for key, value in data.items()
        }

    return data


def get_call_logs_by_company(company_id: str):
    logs = list(call_logs_collection.find({"company_id": company_id}))
    return convert_objectid(logs)


def get_call_logs_by_lead(lead_id: str):
    logs = list(call_logs_collection.find({"lead_id": lead_id}))
    return convert_objectid(logs)


def save_call_log(data: dict):
    data["created_at"] = datetime.utcnow().isoformat()

    result = call_logs_collection.insert_one(data)
    data["_id"] = result.inserted_id

    return convert_objectid(data)