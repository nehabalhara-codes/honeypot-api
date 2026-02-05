from fastapi import FastAPI, Header, HTTPException, Request

app = FastAPI()

API_KEY = "my_secret_key_123"


@app.post("/honeypot")
async def honeypot(
    request: Request,
    x_api_key: str | None = Header(default=None)
):
    # API key validation
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Safe extraction of message text
    text = ""
    try:
        body = await request.json()
        message = body.get("message", {})
        text = message.get("text", "")
    except:
        text = ""

    # Simple scam detection
    scam_keywords = [
        "bank", "account", "blocked", "verify",
        "urgent", "otp", "click"
    ]

    is_scam = any(word in text.lower() for word in scam_keywords)

    # REQUIRED RESPONSE FORMAT
    return {
        "status": "success",
        "reply": (
            "Why is my account being suspended?"
            if is_scam
            else "Thank you for the update."
        )
    }
