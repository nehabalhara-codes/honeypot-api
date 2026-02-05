from fastapi import FastAPI, Header, HTTPException, Request

app = FastAPI(title="Agentic Honey-Pot API")

# =====================
# SECURITY
# =====================
API_KEY = "my_secret_key_123"


def verify_api_key(x_api_key: str | None):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")


# =====================
# HUMAN-LIKE AGENT LOGIC
# =====================
def generate_reply(conversation_history):
    turns = len(conversation_history or [])

    if turns == 0:
        return "Why is my account being suspended? I’m really worried, I use it daily."

    if turns == 1:
        return "Which bank is this about? I have accounts in more than one place."

    if turns == 2:
        return "I didn’t receive any official SMS or email. How do I verify this issue?"

    if turns == 3:
        return "You’re asking for verification, but what exactly do I need to do?"

    if turns == 4:
        return "Do I need to make a payment for verification? If yes, through UPI or something else?"

    if turns == 5:
        return "Please send the UPI ID or QR code. I’m not very comfortable clicking random links."

    return "I’m opening my UPI app now, it’s taking a little time. Please wait."


# =====================
# HONEYPOT ENDPOINT
# =====================
@app.post("/honeypot")
async def honeypot(
    request: Request,
    x_api_key: str | None = Header(default=None)
):
    # 1️⃣ API key check
    verify_api_key(x_api_key)

    # 2️⃣ Safe request parsing (never crashes)
    conversation_history = []
    scam_text = ""

    try:
        body = await request.json()
        conversation_history = body.get("conversationHistory", [])
        message = body.get("message", {})
        scam_text = message.get("text", "")
    except:
        pass

    # 3️⃣ Simple scam detection
    scam_keywords = [
        "bank", "account", "blocked", "verify",
        "urgent", "otp", "payment", "upi", "link"
    ]

    is_scam = any(word in scam_text.lower() for word in scam_keywords)

    # 4️⃣ Agent reply
    reply = (
        generate_reply(conversation_history)
        if is_scam
        else "Thank you for the update."
    )

    # 5️⃣ REQUIRED RESPONSE FORMAT (DO NOT CHANGE)
    return {
        "status": "success",
        "reply": reply
    }
