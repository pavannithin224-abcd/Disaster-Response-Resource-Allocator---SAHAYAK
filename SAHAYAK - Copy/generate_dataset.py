import random
import json
from datetime import datetime, timedelta

CITIES = ["Bengaluru","Mysuru","Mangaluru","Hubli","Belagavi","Tumakuru"]

DISASTERS = {
    "flood": [
        "Heavy floods in {city}, people trapped",
        "Severe flooding reported in {city}",
    ],
    "fire": [
        "Fire broke out in building at {city}",
        "Massive fire accident in {city}",
    ],
    "accident": [
        "Road accident in {city}, multiple injured",
        "Crash reported near {city}",
    ]
}

def random_date():
    start = datetime(2020,1,1)
    end = datetime(2025,1,1)
    return (start + timedelta(
        seconds=random.randint(0, int((end-start).total_seconds()))
    )).strftime("%Y-%m-%d")

data = []

for _ in range(1000):
    dtype = random.choice(list(DISASTERS.keys()))
    template = random.choice(DISASTERS[dtype])
    city = random.choice(CITIES)

    data.append({
        "text": template.format(city=city),
        "date": random_date()
    })

with open("data/tweets.json", "w") as f:
    json.dump(data, f, indent=2)

print("✅ Dataset created!")