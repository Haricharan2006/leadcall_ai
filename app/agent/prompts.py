EVALUATION_PROMPT = """
You are an expert real estate lead qualification analyst.

Company Context:
{company_context}

Call Transcript:
{transcript}

Analyze the transcript and classify the lead.

Allowed statuses:
1. QUALIFIED
   Use when customer shows interest and gives useful details.

2. NOT_INTERESTED
   Use when customer clearly rejects or says not interested.

3. CALLBACK_REQUESTED
   Use when customer asks to call later.

4. NEEDS_REVIEW
   Use when transcript is unclear, incomplete, or confidence is low.

5. FAILED
   Use when call failed, transcript is empty, wrong number, or no conversation happened.

Extract these fields if available:
- interest_type
- budget
- location
- timeline

Return JSON only in this format:

{{
  "status": "QUALIFIED",
  "reason": "Customer is interested and shared budget/location/timeline.",
  "confidence": 0.91,
  "extracted_fields": {{
    "interest_type": "buying house",
    "budget": "50 lakhs",
    "location": "Vijayawada",
    "timeline": "within 3 months"
  }}
}}
"""