from fastapi import APIRouter
from bson import ObjectId
from app.database.mongodb import call_logs_collection

router = APIRouter(prefix="/api/call-logs", tags=["Call Logs"])


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


@router.get("/{company_id}")
def get_call_logs(company_id: str):
    logs = list(call_logs_collection.find({"company_id": company_id}))
    return convert_objectid(logs)


@router.get("/lead/{lead_id}")
def get_lead_call_logs(lead_id: str):
    logs = list(call_logs_collection.find({"lead_id": lead_id}))
    return convert_objectid(logs)