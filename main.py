from fastapi import FastAPI, Header, HTTPException, Request

# 1️⃣ Create app FIRST
app = FastAPI()

# 2️⃣ API key
API_KEY = "my_secret_key_123"

def verify_api_key(x_api_key: str | None):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

# 3️⃣ Honeypot endpoint
@app.post("/honeypot")
async def honeypot(
    request: Request,
    x_api_key: str | None = Header(default=None)
):
    verify_api_key(x_api_key)

    # Read body safely (even if empty or malformed)
    try:
        body = await request.json()
        message = body.get("message", "")
    except:
        message = ""

    scam_keywords = [
        "account", "blocked", "urgent", "click",
        "verify", "bank", "kyc", "payment", "link"
    ]

    scam_detected = any(word in message.lower() for word in scam_keywords)

    reply = (
        "I am not sure what this means. Can you explain?"
        if scam_detected
        else "Thank you for the information."
    )

    return {
        "scam_detected": scam_detected,
        "agent_reply": reply,
        "original_message": message
    }

