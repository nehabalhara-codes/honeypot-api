@app.post("/honeypot")
async def honeypot(
    request: Request,
    x_api_key: Optional[str] = Header(None)
):
    verify_api_key(x_api_key)

    message = "Test message from honeypot validator"

    # Read body ONLY if content-type is JSON
    content_type = request.headers.get("content-type", "")
    if "application/json" in content_type.lower():
        try:
            body = await request.json()
            if isinstance(body, dict) and "message" in body:
                message = body["message"]
        except Exception:
            pass  # ignore all body parsing issues

    scam_detected = is_scam(message)

    return {
        "scam_detected": scam_detected,
        "agent_reply": "Please explain the issue in more detail.",
        "original_message": message
    }
