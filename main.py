from fastapi import FastAPI, Header, HTTPException, Request
from typing import Optional

app = FastAPI(
    title="Agentic Honeypot API",
    version="1.0.0"
)

# =====================
# SECURITY
# =====================
API_KEY = "my_secret_key_123"

def verify_api_key(x_api_key: Optional[str]):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

# =====================
# SCAM LOGIC
# =====================
SCAM_KEYWORDS = [
    "account", "blocked", "urgent", "click",
    "verify", "bank", "kyc", "payment", "link", "upi"
]

def is_scam(message: str) -> bool:
    text = message.lower()
    return any(word in text for word in SCAM_KEYWORDS)

# =====================
# ENDPOINT (NO BODY VALIDATION)
# =====================
@app.post("/honeypot")
async def honeypot(
    request: Request,
    x_api_key: Optional[str] = Header(None)
):
    verify_api_key(x_api_key)

    # Safely read body (if any)
    message = "Test message from honeypot validator"
    try:
        body = await request.json()
        if isinstance(body, dict) and "message" in body:
            message = body["message"]
    except Exception:
        pass  # No body sent (expected for validator)

    scam_detected = is_scam(message)

    return {
        "scam_detected": scam_detected,
        "agent_reply": "Please explain the issue in more detail.",
        "original_message": message
    }


