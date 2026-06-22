# LeadCall AI: Multi-Tenant Agentic Voice Orchestrator

## Project Overview

LeadCall AI is a multi-tenant agentic voice lead qualification platform. It helps companies manage leads, start campaigns, process call transcripts, evaluate customer responses, and update lead statuses automatically.

The project supports multiple tenants/companies such as Green Homes Realty and Urban Rentals. Each company can have separate leads, campaigns, and call logs.

## Features

* Multi-tenant company selection
* Lead directory with add and reset lead options
* Campaign start workflow
* Demo mode for simulated voice call transcripts
* LangGraph-based lead evaluation workflow
* Automatic lead status update
* Call logs with transcript, reason, and confidence score
* Human review section
* Login setup for dashboard access
* MongoDB Atlas cloud database
* Backend deployed on Render
* Frontend deployed on Render

## Tech Stack

### Frontend

* React
* Vite
* Tailwind CSS

### Backend

* FastAPI
* Python
* LangGraph
* Pydantic
* Uvicorn

### Database

* MongoDB Atlas

### Voice Integration

* Vapi AI integration is added for outbound call support.
* Demo mode is used for free demonstration because real outbound phone calls require Vapi telephony credits.

### Deployment

* GitHub for source code hosting
* Render Web Service for backend
* Render Static Site for frontend

## Deployed Links

Frontend Website:

https://leadcall-ai-frontend.onrender.com

Backend API:

https://leadcall-ai-backend.onrender.com

Swagger API Documentation:

https://leadcall-ai-backend.onrender.com/docs

## Source Code

GitHub Repository:

https://github.com/Haricharan2006/leadcall_ai

## Project Architecture

The frontend dashboard communicates with the FastAPI backend using REST APIs. The backend connects to MongoDB Atlas to store companies, leads, campaigns, and call logs.

When a campaign is started, the backend checks pending leads. In demo mode, a simulated transcript is generated for each lead. The transcript is sent to the LangGraph workflow. LangGraph evaluates the transcript and updates the lead status as QUALIFIED, CALLBACK_REQUESTED, NOT_INTERESTED, NEEDS_REVIEW, or FAILED.

The updated status is saved in MongoDB Atlas and displayed in the frontend dashboard.

## Setup Instructions

### Backend Setup

1. Clone the repository:
git clone https://github.com/Haricharan2006/leadcall_ai.git
cd leadcall_ai

2. Create and activate virtual environment:
python -m venv venv
venv\Scripts\activate

3. Install backend dependencies:
pip install -r requirements.txt

4. Create `.env` file and add required values:
MONGO_URI=your_mongodb_atlas_uri
DB_NAME=leadcall_ai
WEBHOOK_SECRET=my_super_secret_123
DEMO_MODE=true
ADMIN_USERNAME=admin
ADMIN_PASSWORD=leadcall123
AUTH_TOKEN=leadcall_demo_token_123
VAPI_API_KEY=your_vapi_api_key
VAPI_ASSISTANT_ID=your_vapi_assistant_id
VAPI_PHONE_NUMBER_ID=your_vapi_phone_number_id
OPENAI_API_KEY=your_openai_api_key

5. Run backend:
uvicorn app.main:app --reload

Backend will run at:
http://127.0.0.1:8000

### Frontend Setup

1. Go to frontend folder:
cd frontend

2. Install frontend dependencies:
npm install

3. Create `.env` file:
VITE_API_BASE_URL=http://127.0.0.1:8000

For deployed backend, use:
VITE_API_BASE_URL=https://leadcall-ai-backend.onrender.com

4. Run frontend: npm run dev

Frontend will run at:
http://localhost:5173


## Demo Login

Username:admin
Password:leadcall123

## Notes on Approach

This project uses demo mode to simulate Vapi voice call transcripts. This allows the complete workflow to be demonstrated without paid telephony credits. The real Vapi integration code is included, and actual phone calling can be enabled by adding valid Vapi API key, assistant ID, phone number ID, and telephony credits.

The project demonstrates the complete flow from lead management to campaign execution, transcript processing, AI evaluation, database update, and frontend visualization.

## Conclusion

LeadCall AI is a complete AI-powered lead qualification dashboard. It combines frontend, backend, database, AI workflow, voice call integration, and cloud deployment into one working project.
