import random

# ✅ DEFINE INCIDENT TEXTS
texts = [
    "Massive fire in building",
    "Earthquake collapsed houses",
    "Flood water rising rapidly",
    "Road accident with injured people",
    "People trapped under debris",
    "Gas explosion in factory",
]


# ✅ AREA LIST
areas = ["Whitefield", "Indiranagar", "BTM", "Electronic City", "Yelahanka"]
import random

SAMPLE_TEXTS = [
    "Fire in building, people trapped",
    "Flood water rising in street",
    "Road blocked due to accident",
    "Need medical help urgently",
    "Power outage in area",
    "Minor traffic jam reported"
]


    

areas = ["Whitefield", "Indiranagar", "BTM", "Electronic City", "Yelahanka"]

def generate_incident():
    return {
        "text": random.choice(texts),
        "lat": random.uniform(12.85, 13.05),
        "lon": random.uniform(77.50, 77.75),
        "area": random.choice(areas)   # ✅ ADD THIS
    }