import random
import time

CITIES = ["Bengaluru","Mysuru","Hubli","Mangaluru"]

TEMPLATES = [
    "Flood reported in {city}",
    "Fire accident in {city}",
    "Road accident in {city}",
    "Medical emergency in {city}"
]

def stream_data():
    while True:
        yield {
            "text": random.choice(TEMPLATES).format(
                city=random.choice(CITIES)
            )
        }
        time.sleep(0.5)   # simulate live data