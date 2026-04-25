import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(layout="wide")

import time
import folium
from streamlit_folium import st_folium

from data_generator import generate_incident
from ai_engine import classify_severity, assign_resources
from news_feed import fetch_disaster_news

# OPTIONAL IMPORT
try:
    from predictor import predict_area_risk
    has_predictor = True
except:
    has_predictor = False

st.title("🚨 AI Disaster Response Command Center")

# ---------------- FLASHING P1 CSS ----------------
st.markdown("""
<style>
@keyframes blink {
    0% {opacity: 1;}
    50% {opacity: 0.2;}
    100% {opacity: 1;}
}
.p1-alert {
    color: white;
    background-color: red;
    padding: 8px;
    border-radius: 8px;
    font-weight: bold;
    animation: blink 1s infinite;
}
</style>
""", unsafe_allow_html=True)

# ---------------- PRIORITY FUNCTION ----------------
def compute_priority(text, severity):
    text = text.lower()
    score = 0

    if "earthquake" in text:
        score += 100
    if "flood" in text:
        score += 95
    if "trapped" in text:
        score += 90
    if "fire" in text:
        score += 70
    if "injured" in text:
        score += 60

    if severity == "HIGH":
        score += 50
    elif severity == "MEDIUM":
        score += 20

    if score >= 140:
        return "P1"
    elif score >= 100:
        return "P2"
    elif score >= 60:
        return "P3"
    else:
        return "P4"

# ---------------- RESOURCE ICON ----------------
def get_icon(resource):
    if "Ambulance" in resource:
        return folium.Icon(color="red", icon="plus")
    elif "Fire" in resource:
        return folium.Icon(color="orange", icon="fire")
    elif "Police" in resource:
        return folium.Icon(color="blue", icon="shield")
    else:
        return folium.Icon(color="green")

# ---------------- MULTI VEHICLE CREATION ----------------
def create_vehicles(incident, base):
    vehicles = []

    for res in incident["resources"]:
        count = 2 if incident["priority"] == "P1" else 1

        for _ in range(count):
            vehicles.append({
                "target": [incident["lat"], incident["lon"]],
                "current": base.copy(),
                "step_lat": (incident["lat"] - base[0]) / 20,
                "step_lon": (incident["lon"] - base[1]) / 20,
                "active": True,
                "resource": res
            })

    return vehicles

# ---------------- VEHICLE MOVEMENT ----------------
def update_vehicles():
    for v in st.session_state.vehicles:
        if v["active"]:
            v["current"][0] += v["step_lat"]
            v["current"][1] += v["step_lon"]

            if abs(v["current"][0] - v["target"][0]) < 0.001:
                v["active"] = False

# ---------------- SESSION ----------------
if "data" not in st.session_state:
    st.session_state.data = []

if "last_update" not in st.session_state:
    st.session_state.last_update = time.time()

if "dispatch_status" not in st.session_state:
    st.session_state.dispatch_status = {
        "Food": False,
        "Clothes": False,
        "Water": False,
        "Medical Kits": False,
        "Blankets": False
    }

if "vehicles" not in st.session_state:
    st.session_state.vehicles = []

# ---------------- AUTO INCIDENT ----------------
now = time.time()

if now - st.session_state.last_update >= 8:
    incident = generate_incident()

    severity, score = classify_severity(incident["text"])
    resources = assign_resources(severity, incident["text"])
    priority = compute_priority(incident["text"], severity)

    incident.update({
        "severity": severity,
        "resources": resources,
        "priority": priority,
        "timestamp": now
    })

    base_location = [12.97, 77.59]
    new_vehicles = create_vehicles(incident, base_location)
    st.session_state.vehicles.extend(new_vehicles)

    st.session_state.data.append(incident)
    st.session_state.last_update = now

# UPDATE VEHICLES
update_vehicles()

# ---------------- LAYOUT ----------------
left, middle, right = st.columns([1.2, 1.2, 2])

# ================= LEFT =================
with left:
    st.subheader("📡 Live Incidents")

    for item in reversed(st.session_state.data[-8:]):

        if item["priority"] == "P1":
            st.markdown(
                f"<div class='p1-alert'>🚨 P1 EMERGENCY: {item['text']}</div>",
                unsafe_allow_html=True
            )
        else:
            st.write(f"🔥 {item['severity']} - {item['text']}")

        st.write(f"🚨 Priority: {item['priority']}")
        st.caption(f"🚑 {item['resources']}")
        st.divider()

    st.subheader("🌍 Live News")

    news = fetch_disaster_news()
    for n in news[:5]:
        st.write(f"📰 {n.get('title', 'No Title')}")

# ================= MIDDLE =================
with middle:
    st.subheader("📦 Relief Dispatch System")

    for k, v in st.session_state.dispatch_status.items():
        col1, col2 = st.columns([2, 1])

        with col1:
            st.write(f"📌 {k}")

        with col2:
            st.success("Delivered ✔" if v else "Pending ❌")

    if st.button("🚀 Trigger Dispatch"):
        for k in st.session_state.dispatch_status:
            time.sleep(0.3)
            st.session_state.dispatch_status[k] = True
        st.success("All resources dispatched!")

# ================= RIGHT =================
with right:
    st.subheader("🗺️ Live Incident Map")

    base_location = [12.97, 77.59]

    m = folium.Map(location=base_location, zoom_start=11, control_scale=True)

    # INCIDENT MARKERS
    for item in st.session_state.data[-10:]:
        color = "red" if item["severity"] == "HIGH" else "orange" if item["severity"] == "MEDIUM" else "green"

        folium.CircleMarker(
            location=[item["lat"], item["lon"]],
            radius=8,
            color=color,
            fill=True,
            fill_opacity=0.7,
            popup=f"{item['text']} | {item['priority']}"
        ).add_to(m)

    # VEHICLES
    for v in st.session_state.vehicles:
        folium.Marker(
            location=v["current"],
            icon=get_icon(v["resource"]),
            popup=f"{v['resource']} moving"
        ).add_to(m)

    st_folium(m, width=750, height=520, key="map")

# ---------------- OPTIONAL PREDICTION ----------------
if has_predictor:
    st.sidebar.subheader("🔮 Area-wise Risk Prediction")

    predictions = predict_area_risk(st.session_state.data)

    for p in predictions:
        st.sidebar.markdown(f"""
        📍 **{p['area']}**  
        🚨 Risk: **{p['risk']}**  
        📊 Score: {p['score']}
        """)

# ---------------- AUTO REFRESH ----------------
time.sleep(1)
st.rerun()