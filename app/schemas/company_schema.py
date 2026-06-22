from pydantic import BaseModel
from typing import List, Dict, Any

class CompanyCreate(BaseModel):
    company_id: str
    name: str
    industry: str
    business_type: str
    prompt_instructions: str
    qualification_questions: List[str]
    qualification_rules: Dict[str, Any]