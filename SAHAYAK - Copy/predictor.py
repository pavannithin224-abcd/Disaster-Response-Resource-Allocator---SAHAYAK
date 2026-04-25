from collections import defaultdict
import random

def predict_area_risk(data):

    area_scores = defaultdict(list)

    # collect severity per area
    for d in data:
        area = d.get("area", "Unknown")

        if d["severity"] == "HIGH":
            area_scores[area].append(1)
        elif d["severity"] == "MEDIUM":
            area_scores[area].append(0.5)
        else:
            area_scores[area].append(0.2)

    results = []

    for area, scores in area_scores.items():
        avg = sum(scores) / len(scores)

        if avg > 0.7:
            risk = "HIGH"
        elif avg > 0.4:
            risk = "MEDIUM"
        else:
            risk = "LOW"

        results.append({
            "area": area,
            "risk": risk,
            "score": round(avg, 2)
        })

    # sort by highest risk
    results = sorted(results, key=lambda x: x["score"], reverse=True)

    return results[:3]   # ✅ top 3 areas