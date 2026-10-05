def sanitize_memory_payload(raw_history):
    """
    Omni-Industrial Context Engine.
    Acts as a sanitary firewall between the UI and the Core Router.
    Strips UI-specific tags (like 'audio') that crash the Groq API.
    Enforces strict token limits by retaining only the last 10 interactions.
    """
    clean_history = []
    for msg in raw_history:
        if msg.get("role") in ["user", "assistant"] and msg.get("content"):
            clean_history.append({"role": msg["role"], "content": msg["content"]})
            
    return clean_history[-10:]
