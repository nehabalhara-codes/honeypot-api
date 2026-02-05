from fastapi import FastAPI, Header, HTTPException, Request

app = FastAPI(
    title="Agentic Honeypot API",
    version="1.0.0"
)

# =====================
# SECURITY
# =====================
API_KEY = "my_secret_key_123"

def verify_api_key(x_api_key: str | None):
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
    return any(word in message.lower() for word in SCAM_KEYWORDS)

# =====================
# ENDPOINT (NO BODY VALIDATION)
# =====================
@app.post("/honeypot")
async def honeypot(
    request: Request,
    x_api_key: str | None = Header(None)
):
    verify_api_key(x_api_key)

    # Try to read JSON body if present (optional)
    try:
        body = await request.json()
        message = body.get("message", "Test message from honeypot validator")
    except Exception:
        message = "Test message from honeypot validator"

    scam_detected = is_scam(message)

    return {
        "scam_detected": scam_detected,
        "agent_reply": "Please explain the issue in more detail.",
        "original_message": message
    }
