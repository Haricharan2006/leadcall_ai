from pydantic import BaseModel

class LeadCreate(BaseModel):
    company_id: str
    name: str
    phone: str