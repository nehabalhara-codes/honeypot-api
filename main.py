from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="Agentic Honeypot API",
    description="Detects scam messages and simulates a honeypot agent",
    version="1.0.0"
)

# =====================
# SECURITY
# =====================
API_KEY = "my_secret_key_123"

def verify_api_key(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized: Invalid API Key"
        )

# =====================
# REQUEST MODEL
# =====================
class MessageRequest(BaseModel):
    message: Optional[str] = None

# =====================
# SCAM DETECTION LOGIC
# =====================
SCAM_KEYWORDS = [
    "account",
    "blocked",
    "urgent",
    "click",
    "verify",
    "bank",
    "kyc",
    "payment",
    "link",
    "upi"
]

def is_scam(message: str) -> bool:
    text = message.lower()
    return any(keyword in text for keyword in SCAM_KEYWORDS)

# =====================
# HONEYPOT ENDPOINT
# =====================
@app.post("/honeypot")
def honeypot(
    data: Optional[MessageRequest] = None,
    x_api_key: str = Header(None)
):
    verify_api_key(x_api_key)

    # Handle missing request body (required for official tester)
    message = (
        data.message
        if data and data.message
        else "Test message from honeypot validator"
    )

    scam_detected = is_scam(message)

    agent_reply = (
        "Please explain the issue in more detail so I can resolve it."
        if scam_detected
        else "Thank you for the information."
    )

    return {
        "scam_detected": scam_detected,
        "agent_reply": agent_reply,
        "original_message": message
    }
