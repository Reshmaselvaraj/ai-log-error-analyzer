def classify_error(message):
    msg = message.lower()

    if "database" in msg or "db" in msg:
        return "DATABASE"
    elif "timeout" in msg:
        return "TIMEOUT"
    elif "api" in msg:
        return "API"
    elif "memory" in msg:
        return "MEMORY"
    else:
        return "UNKNOWN"
