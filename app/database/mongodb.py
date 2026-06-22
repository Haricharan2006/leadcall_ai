from pymongo import MongoClient
from app.core.config import settings

client = MongoClient(
    settings.MONGO_URI,
    tls=True,
    tlsAllowInvalidCertificates=True,
    serverSelectionTimeoutMS=30000,
    connectTimeoutMS=30000
)

db = client[settings.DB_NAME]

companies_collection = db["companies"]
leads_collection = db["leads"]
campaigns_collection = db["campaigns"]
call_logs_collection = db["call_logs"]