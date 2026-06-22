from typing import TypedDict, Optional, Dict, Any


class LeadEvaluationState(TypedDict, total=False):
    lead_id: str
    company_id: str
    transcript: str

    company_context: Optional[str]
    raw_llm_response: Optional[str]

    status: Optional[str]
    reason: Optional[str]
    confidence: Optional[float]
    extracted_fields: Optional[Dict[str, Any]]

    evaluation_source: Optional[str]
    error: Optional[str]