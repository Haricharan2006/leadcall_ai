from fastapi import APIRouter, HTTPException
from bson import ObjectId
from app.database.mongodb import companies_collection

router = APIRouter(prefix="/api/companies", tags=["Companies"])


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


@router.get("")
def get_companies():
    try:
        companies = list(companies_collection.find({}))
        return convert_objectid(companies)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{company_id}")
def get_company(company_id: str):
    try:
        company = companies_collection.find_one({"company_id": company_id})

        if company is None:
            raise HTTPException(status_code=404, detail="Company not found")

        return convert_objectid(company)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))