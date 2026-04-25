# ---------------- SEVERITY CLASSIFICATION ----------------
def classify_severity(text):
    text = text.lower()

    if "earthquake" in text or "collapse" in text or "trapped" in text:
        return "HIGH", 0.9

    elif "fire" in text or "injured" in text or "accident" in text:
        return "MEDIUM", 0.6

    else:
        return "LOW", 0.3


# ---------------- RESOURCE ASSIGNMENT ----------------
def assign_resources(severity, text=""):
    text = text.lower()
    resources = []

    # 🔥 FIRE
    if "fire" in text:
        resources.extend(["Fire Force", "Ambulance"])

    # 🌊 FLOOD / EARTHQUAKE
    if "flood" in text or "earthquake" in text:
        resources.extend(["Ambulance", "Fire Force", "Police"])

    # 🚑 MEDICAL
    if "injured" in text or "accident" in text:
        resources.extend(["Ambulance", "Police"])

    # 🚓 LAW
    if "crowd" in text or "violence" in text:
        resources.append("Police")

    # fallback
    if not resources:
        if severity == "HIGH":
            resources = ["Ambulance", "Fire Force", "Police"]
        elif severity == "MEDIUM":
            resources = ["Ambulance", "Police"]
        else:
            resources = ["Police"]

    return list(set(resources))