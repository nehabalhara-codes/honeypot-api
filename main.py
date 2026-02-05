from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import re

app = FastAPI()

# ================= SECURITY =================
API_KEY = "my_secret_key_123"

def verify_api_key(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")


# ================= REQUEST MODEL =================
class MessageRequest(BaseModel):
    message: str
    conversation_id: str | None = "default"


# ================= MEMORY =================
# Stores conversation history
conversations = {}


# ================= SCAM DETECTION =================
SCAM_KEYWORDS = [
    "account", "blocked", "urgent", "click",
    "verify", "bank", "kyc", "payment",
    "transfer", "link"
]

def is_scam(message: str) -> tuple[bool, float]:
    msg = message.lower()
    matched = [w for w in SCAM_KEYWORDS if w in msg]
    confidence = min(0.95, len(matched) * 0.15)
    return len(matched) > 0, round(confidence, 2)


# ================= INTELLIGENCE EXTRACTION =================
def extract_intelligence(text: str):
    return {
        "upi_ids": re.findall(r"[a-zA-Z0-9.\-_]{2,}@[a-zA-Z]{2,}", text),
        "urls": re.findall(r"https?://\S+", text),
        "bank_account_numbers": re.findall(r"\b\d{9,18}\b", text),
    }


# ================= AGENT LOGIC =================
def agent_reply(turns: int):
    if turns == 1:
        return "I just received this message. What exactly do I need to do?"
    elif turns == 2:
        return "They are asking me to act fast. Is this really from the bank?"
    else:
        return "Can you please share the official link or account details?"


# ================= API ENDPOINT =================
@app.post("/honeypot")
def receive_message(
    data: MessageRequest,
    x_api_key: str = Header(None)
):
    verify_api_key(x_api_key)

    message = data.message
    conv_id = data.conversation_id

    # Store conversation
    history = conversations.get(conv_id, [])
    history.append({"from": "scammer", "text": message})
    conversations[conv_id] = history

    turns = len(history)

    # Scam detection
    scam_detected, confidence_score = is_scam(message)

    # Agent response
    reply = agent_reply(turns) if scam_detected else "Thank you for the information."

    # Intelligence extraction
    intelligence = extract_intelligence(message)

    return {
        "scam_detected": scam_detected,
        "confidence_score": confidence_score,
        "conversation_id": conv_id,
        "turns": turns,
        "agent_reply": reply,
        "extracted_intelligence": intelligence,
        "original_message": message
    }

