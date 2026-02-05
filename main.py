from fastapi import FastAPI, Header, HTTPException, Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="Agentic Honeypot API",
    version="1.0.0"
)

# =====================
# SECURITY
# =====================
API_KEY = "my_secret_key_123"

def verify_api_key(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

# =====================
# REQUEST MODEL
# =====================
class MessageRequest(BaseModel):
    message: Optional[str] = None

# =====================
# SCAM LOGIC
# =====================
SCAM_KEYWORDS = [
    "account", "blocked", "urgent", "click",
    "verify", "bank", "kyc", "payment", "link", "upi"
]

def is_scam(message: str) -> bool:
    return any(word in message.lower() for word in SCAM_KEYWORDS)

# =====================
# ENDPOINT
# =====================
@app.post("/honeypot")
def honeypot(
    data: Optional[MessageRequest] = Body(None),
    x_api_key: str = Header(None)
):
    verify_api_key(x_api_key)

    # Handle empty body (official tester case)
    message = (
        data.message
        if data and data.message
        else "Test message from honeypot validator"
    )

    scam = is_scam(message)

    return {
        "scam_detected": scam,
        "agent_reply": "Please explain the issue in more detail.",
        "original_message": message
    }
