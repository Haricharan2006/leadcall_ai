import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    MONGO_URI = os.getenv("MONGO_URI")
    DB_NAME = os.getenv("DB_NAME", "leadcall_ai")

    VAPI_API_KEY = os.getenv("VAPI_API_KEY", "")
    VAPI_ASSISTANT_ID = os.getenv("VAPI_ASSISTANT_ID", "")
    VAPI_PHONE_NUMBER_ID = os.getenv("VAPI_PHONE_NUMBER_ID", "")

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

    WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "my_super_secret_123")


settings = Settings()