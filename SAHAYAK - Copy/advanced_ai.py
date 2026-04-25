from transformers import pipeline

# Zero-shot classification (powerful & flexible)
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

labels = [
    "earthquake emergency",
    "flood disaster",
    "fire accident",
    "medical emergency",
    "road accident",
    "minor issue"
]

def classify_disaster(text):
    result = classifier(text, candidate_labels=labels)
    return result["labels"][0], result["scores"][0]


def advanced_priority(text, severity, confidence):

    score = 0
    text = text.lower()

    # AI confidence
    score += confidence * 100

    # disaster type weight
    if "earthquake" in text or "flood" in text:
        score += 100
    elif "fire" in text:
        score += 70
    elif "accident" in text:
        score += 50

    # severity boost
    if severity == "HIGH":
        score += 50
    elif severity == "MEDIUM":
        score += 25

    # decision
    if score > 150:
        return "P1"
    elif score > 110:
        return "P2"
    elif score > 70:
        return "P3"
    else:
        return "P4"


# ✅ FIXED: moved outside (was wrongly indented inside function)
def smart_dispatch(priority, disaster_type):

    if priority == "P1":
        return ["Ambulance", "Fire Force", "Rescue Team", "Police"]

    elif priority == "P2":
        return ["Ambulance", "Rescue Team"]

    elif priority == "P3":
        return ["Medical Support"]

    else:
        return ["Monitor"]