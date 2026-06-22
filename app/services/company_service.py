from bson import ObjectId
from app.database.mongodb import companies_collection


def convert_objectid(data):
    if isinstance(data, list):
        return [convert_objectid(item) for item in data]

    if isinstance(data, dict):
        return {
            key: str(value) if isinstance(value, ObjectId) else convert_objectid(value)
            for key, value in data.items()
        }

    return data


def get_all_companies():
    companies = list(companies_collection.find({}))
    return convert_objectid(companies)


def get_company_by_id(company_id: str):
    company = companies_collection.find_one({"company_id": company_id})

    if not company:
        return None

    return convert_objectid(company)