from fastapi import APIRouter
from app.database.mongodb import leads_collection, call_logs_collection

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


@router.get("/{company_id}")
def get_analytics(company_id: str):
    total = leads_collection.count_documents({"company_id": company_id})
    pending = leads_collection.count_documents({"company_id": company_id, "status": "PENDING"})
    call_initiated = leads_collection.count_documents({"company_id": company_id, "status": "CALL_INITIATED"})
    qualified = leads_collection.count_documents({"company_id": company_id, "status": "QUALIFIED"})
    not_interested = leads_collection.count_documents({"company_id": company_id, "status": "NOT_INTERESTED"})
    callback_requested = leads_collection.count_documents({"company_id": company_id, "status": "CALLBACK_REQUESTED"})
    needs_review = leads_collection.count_documents({"company_id": company_id, "status": "NEEDS_REVIEW"})
    failed = leads_collection.count_documents({"company_id": company_id, "status": "FAILED"})
    call_logs_count = call_logs_collection.count_documents({"company_id": company_id})

    return {
        "company_id": company_id,
        "total_leads": total,
        "pending": pending,
        "call_initiated": call_initiated,
        "qualified": qualified,
        "not_interested": not_interested,
        "callback_requested": callback_requested,
        "needs_review": needs_review,
        "failed": failed,
        "call_logs": call_logs_count
    }