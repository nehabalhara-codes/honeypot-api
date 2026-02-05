from fastapi import FastAPI, Header, HTTPException, Request

app = FastAPI()

API_KEY = "my_secret_key_123"


@app.post("/honeypot")
async def honeypot(
    request: Request,
    x_api_key: str | None = Header(default=None)
):
    # API key check
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # SAFE body handling (never crashes)
    message = ""
    try:
        body = await request.json()
        if isinstance(body, dict):
            message = str(body.get("message", ""))
    except:
        message = ""

    # Simple scam detection
    scam_keywords = [
        "bank", "account", "blocked", "urgent",
        "click", "verify", "kyc", "payment", "link"
    ]

    scam_detected = any(word in message.lower() for word in scam_keywords)

    return {
        "scam_detected": scam_detected,
        "agent_reply": (
            "I am not sure about this. Can you explain what I need to do?"
            if scam_detected
            else "Thank you for the information."
        ),
        "extracted_intelligence": {
            "bank_accounts": [],
            "upi_ids": [],
            "phishing_links": []
        }
    }
