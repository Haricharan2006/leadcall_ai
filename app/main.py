from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.company_routes import router as company_router
from app.routes.lead_routes import router as lead_router
from app.routes.call_log_routes import router as call_log_router
from app.routes.analytics_routes import router as analytics_router
from app.routes.campaign_routes import router as campaign_router
from app.routes.webhook_routes import router as webhook_router

app = FastAPI(
    title="LeadCall AI",
    description="Multi-Tenant Agentic Voice Orchestrator",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(company_router)
app.include_router(lead_router)
app.include_router(call_log_router)
app.include_router(analytics_router)
app.include_router(campaign_router)
app.include_router(webhook_router)

@app.get("/")
def root():
    return {
        "app": "LeadCall AI",
        "status": "running",
        "message": "Multi-Tenant Agentic Voice Orchestrator backend is live"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }