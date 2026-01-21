def assign_severity(level, category):
    if level == "ERROR":
        return "HIGH"
    if level == "WARN":
        return "MEDIUM"
    return "LOW"
