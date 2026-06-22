from fastapi import APIRouter, HTTPException, Header, Body
from app.core.config import settings

router = APIRouter(prefix="/api/webhooks", tags=["Webhooks"])


@router.post("/vapi")
async def handle_vapi_webhook(
    payload: dict = Body(...),
    x_webhook_secret: str | None = Header(default=None)
):
    expected_secret = getattr(settings, "WEBHOOK_SECRET", "my_super_secret_123")

    if x_webhook_secret != expected_secret:
        raise HTTPException(status_code=401, detail="Invalid webhook secret")

    message = payload.get("message", {})
    call = message.get("call", {})
    metadata = call.get("metadata", {})

    lead_id = metadata.get("lead_id")
    company_id = metadata.get("company_id")

    transcript = (
        message.get("transcript")
        or message.get("summary")
        or payload.get("transcript")
        or "No transcript available"
    )

    if not lead_id or not company_id:
        raise HTTPException(
            status_code=400,
            detail="Missing lead_id or company_id in webhook metadata"
        )

    from app.agent.graph import lead_evaluation_graph

    result = lead_evaluation_graph.invoke({
        "lead_id": lead_id,
        "company_id": company_id,
        "transcript": transcript,
        "company_context": None,
        "raw_llm_response": None,
        "status": None,
        "reason": None,
        "confidence": None,
        "extracted_fields": None
    })

    return {
        "message": "Webhook processed successfully",
        "lead_id": lead_id,
        "company_id": company_id,
        "final_status": result["status"],
        "confidence": result["confidence"]
    }