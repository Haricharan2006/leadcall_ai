from datetime import datetime
from app.database.mongodb import (
    companies_collection,
    leads_collection,
    campaigns_collection,
    call_logs_collection
)

def seed_database():
    companies_collection.delete_many({})
    leads_collection.delete_many({})
    campaigns_collection.delete_many({})
    call_logs_collection.delete_many({})

    now = datetime.utcnow().isoformat()

    companies = [
        {
            "company_id": "green_homes",
            "name": "Green Homes Realty",
            "industry": "Real Estate Sales",
            "business_type": "property_sales",
            "prompt_instructions": "You help customers interested in buying residential houses.",
            "qualification_questions": [
                "Are you looking to buy a property?",
                "What is your approximate budget?",
                "Which location are you interested in?",
                "When are you planning to buy?"
            ],
            "qualification_rules": {
                "minimum_required_fields": ["budget", "location", "timeline"],
                "needs_review_confidence_threshold": 0.65
            },
            "created_at": now
        },
        {
            "company_id": "urban_rentals",
            "name": "Urban Rentals",
            "industry": "Apartment Rentals",
            "business_type": "rental_apartments",
            "prompt_instructions": "You help customers interested in renting apartments.",
            "qualification_questions": [
                "Are you looking for a rental apartment?",
                "What is your monthly rental budget?",
                "Which area do you prefer?",
                "When do you want to move in?"
            ],
            "qualification_rules": {
                "minimum_required_fields": ["budget", "location", "timeline"],
                "needs_review_confidence_threshold": 0.65
            },
            "created_at": now
        }
    ]

    leads = [
        {
            "lead_id": "lead_001",
            "company_id": "green_homes",
            "name": "Ravi Kumar",
            "phone": "+91XXXXXXXXXX",
            "status": "PENDING",
            "interest_type": None,
            "budget": None,
            "location": None,
            "timeline": None,
            "last_call_id": None,
            "last_campaign_id": None,
            "attempt_count": 0,
            "created_at": now,
            "updated_at": now
        },
        {
            "lead_id": "lead_002",
            "company_id": "green_homes",
            "name": "Kiran Reddy",
            "phone": "+91XXXXXXXXXX",
            "status": "PENDING",
            "interest_type": None,
            "budget": None,
            "location": None,
            "timeline": None,
            "last_call_id": None,
            "last_campaign_id": None,
            "attempt_count": 0,
            "created_at": now,
            "updated_at": now
        },
        {
            "lead_id": "lead_003",
            "company_id": "urban_rentals",
            "name": "Sita Sharma",
            "phone": "+91XXXXXXXXXX",
            "status": "PENDING",
            "interest_type": None,
            "budget": None,
            "location": None,
            "timeline": None,
            "last_call_id": None,
            "last_campaign_id": None,
            "attempt_count": 0,
            "created_at": now,
            "updated_at": now
        },
        {
            "lead_id": "lead_004",
            "company_id": "urban_rentals",
            "name": "Arjun Mehta",
            "phone": "+91XXXXXXXXXX",
            "status": "PENDING",
            "interest_type": None,
            "budget": None,
            "location": None,
            "timeline": None,
            "last_call_id": None,
            "last_campaign_id": None,
            "attempt_count": 0,
            "created_at": now,
            "updated_at": now
        }
    ]

    companies_collection.insert_many(companies)
    leads_collection.insert_many(leads)

    print("Advanced seed data inserted successfully")

if __name__ == "__main__":
    seed_database()