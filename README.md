# SAHAYAK: Disaster Response Command Center

A live dashboard that turns incoming emergency reports into a **priority level, a resource dispatch and a moving map**. Built by a 4-member team at the **Nexora Hackathon 2025 (Bengaluru)** and taken from idea to a working demo within the time limit.

> **Status: hackathon prototype.** Incidents are simulated and the rules are hand-written. It has not been tested against real emergency data, and there are no accuracy figures. What it does show is the full flow, from report to dispatch, working end to end.

## What it does

| Step | What happens |
|---|---|
| 1. Report comes in | A new incident (fire, flood, earthquake, accident, trapped people) is generated every 8 seconds |
| 2. Severity | Keyword rules grade it HIGH / MEDIUM / LOW (`ai_engine.py`) |
| 3. Priority | A score turns text + severity into **P1 to P4**; P1 flashes red on the dashboard |
| 4. Resources | The right units are picked (Ambulance, Fire Force, Police) and vehicles are drawn moving from the Bengaluru base to the incident (2 units per resource on P1) |
| 5. Relief dispatch | Food, Clothes, Water, Medical Kits and Blankets tracked as Pending / Delivered, with a one-click dispatch |
| 6. Context | Live disaster headlines pulled from the GDELT news API |

A second pipeline (`pipeline.py`) maps free-text reports to Bengaluru areas (Silk Board, BTM, Koramangala, Bellandur, Whitefield, Marathahalli, HSR, Indiranagar). It then assigns the nearest available unit from `data/resources.json` and sizes food and clothing relief from the area's estimated population.

## Where the AI is, honestly

- **Core dashboard (`app.py`):** rule-based severity, priority and dispatch. Fast, predictable and explainable, with no model download needed.
- **Optional (`advanced_ai.py`):** zero-shot classification with `facebook/bart-large-mnli` across six emergency types, feeding a confidence-weighted priority score. `download_models.py` fetches the models (BART, a NER model and MiniLM) before first use.
- **Risk view (`predictor.py`):** averages severity per area and returns the top 3 highest-risk areas.

## Run it

```bash
pip install -r requirements.txt
streamlit run app.py
```

The core dashboard needs only Streamlit, folium, streamlit-folium, pandas, numpy and requests. The transformer models are needed only for the optional `advanced_ai.py`.

## Limits and next steps

- Incident data is simulated; the next step is a real feed (emergency calls, verified social posts).
- Rules are keyword-based, so they will miss phrasing they were not written for. They should be tested on a labelled set of real reports.
- Vehicle movement is a straight line, not road routing.
- Relief quantities use rough population estimates.

## Tech

Python, Streamlit, folium, Hugging Face Transformers (optional), GDELT API.

*Team project, Nexora Hackathon 2025. Author of this repository: Pavan D, [GitHub](https://github.com/pavannithin224-abcd).*
