import random

# ───── LOCATION DATABASE ─────
LOCATIONS = {
    "silk board": (12.917, 77.623),
    "btm": (12.916, 77.61),
    "koramangala": (12.935, 77.624),
    "bellandur": (12.925, 77.675),
    "whitefield": (12.9698, 77.7500),
    "marathahalli": (12.9591, 77.7019),
    "hsr": (12.9116, 77.6389),
    "indiranagar": (12.9784, 77.6408),
}

base_location = [12.97, 77.59]  # Bangalore base

# ───── RESOURCE MAP ─────
RESOURCE_MAP = {
    "medical emergency": ["ambulance"],
    "fire emergency": ["fire_truck"],
    "flood rescue": ["rescue_team"],
    "road accident": ["ambulance"]
}

# ───── POPULATION ESTIMATE (FOR FOOD + CLOTHING) ─────
POPULATION = {
    "silk board": 5000,
    "btm": 8000,
    "koramangala": 6000,
    "bellandur": 7000,
    "whitefield": 9000,
    "marathahalli": 6500,
    "hsr": 7500,
    "indiranagar": 5500,
}

# ───── CLASSIFIER (FAST RULE BASED) ─────
def classify(text):
    text = text.lower()

    if "flood" in text:
        return "flood rescue"
    elif "fire" in text:
        return "fire emergency"
    elif "accident" in text:
        return "road accident"
    else:
        return "medical emergency"

# ───── LOCATION DETECTION ─────
def get_location(text):
    text = text.lower()

    for k, v in LOCATIONS.items():
        if k in text:
            return k, v[0], v[1]

    return "bengaluru", 12.97, 77.59

# ───── SCORE CALCULATION ─────
def score(text):
    s = 5
    if "urgent" in text.lower():
        s += 2
    if "trapped" in text.lower():
        s += 3
    return min(s, 10)

# ───── RESOURCE ALLOCATION ─────
def allocate(resources, etype, location):

    needed = RESOURCE_MAP.get(etype, ["ambulance"])

    # find emergency unit
    unit = None
    for r in resources:
        if r["type"] in needed and r["status"] == "available":
            r["status"] = "busy"
            unit = r
            break

    # POPULATION BASED RELIEF CALCULATION
    pop = POPULATION.get(location, 3000)

    food = max(1, pop // 2000)
    clothing = max(1, pop // 2500)

    return unit, food, clothing

# ───── MAIN PROCESSOR ─────
def process_tweet(tweet, resources):

    text = tweet["text"]

    etype = classify(text)
    loc, lat, lon = get_location(text)
    sc = score(text)

    unit, food, clothing = allocate(resources, etype, loc)

    return {
        "text": text,
        "type": etype,
        "score": sc,
        "lat": lat,
        "lon": lon,
        "unit": unit,
        "food": food,
        "clothing": clothing
    }