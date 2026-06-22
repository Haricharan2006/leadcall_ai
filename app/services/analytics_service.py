from app.database.mongodb import leads_collection, call_logs_collection


def get_company_analytics(company_id: str):
    return {
        "company_id": company_id,
        "total_leads": leads_collection.count_documents({"company_id": company_id}),
        "pending": leads_collection.count_documents({
            "company_id": company_id,
            "status": "PENDING"
        }),
        "call_initiated": leads_collection.count_documents({
            "company_id": company_id,
            "status": "CALL_INITIATED"
        }),
        "qualified": leads_collection.count_documents({
            "company_id": company_id,
            "status": "QUALIFIED"
        }),
        "not_interested": leads_collection.count_documents({
            "company_id": company_id,
            "status": "NOT_INTERESTED"
        }),
        "callback_requested": leads_collection.count_documents({
            "company_id": company_id,
            "status": "CALLBACK_REQUESTED"
        }),
        "needs_review": leads_collection.count_documents({
            "company_id": company_id,
            "status": "NEEDS_REVIEW"
        }),
        "failed": leads_collection.count_documents({
            "company_id": company_id,
            "status": "FAILED"
        }),
        "call_logs": call_logs_collection.count_documents({
            "company_id": company_id
        })
    }