"""The single integration seam between the dashboard and the Ceph agent.

Today every accessor returns fixtures from ``static_data``. Tomorrow, set

    CEPH_API_URL=https://<didier-endpoint>

as an environment variable or in ``.streamlit/secrets.toml`` and the same functions
issue HTTP calls instead. No UI file changes, no layout changes.

--------------------------------------------------------------------------------
EXPECTED JSON CONTRACT (what the agent should return)
--------------------------------------------------------------------------------
GET  {CEPH_API_URL}/shipments
     -> {"shipments": ["CN-SZ-TR-5567", "DK-AAR-RD-2210"]}

GET  {CEPH_API_URL}/shipments/{id}
     -> {"shipment_id", "container", "customer", "origin", "destination", "cargo",
         "weight_kg" (number), "priority", "deadline", "current_location",
         "current_status", "latest_tracking", "disruption", "eta",
         "hours_to_deadline" (number), "baseline_route", "recommended_route",
         "legs": [str]}

GET  {CEPH_API_URL}/shipments/{id}/routes
     -> {"routes": [{"route", "label", "co2e_kg" (number),
                     "transit_hours" (number), "hours_before_deadline" (number),
                     "cost_eur" (number), "modes", "baseline" (bool)}]}

GET  {CEPH_API_URL}/shipments/{id}/decisions
     -> {"decisions": [{"id", "title", "confidence" (0-100 number),
                        "classification", "action", "rationale": [str]}]}

GET  {CEPH_API_URL}/ingestion
     -> {"feed": [{"format", "name", "source", "status", "records" (number)}]}

POST {CEPH_API_URL}/chat            body: {"question": str, "shipment_id": str|null}
     -> {"answer": "markdown string"}

POST {CEPH_API_URL}/feedback        body: {"decision_id", "verdict": "approved"|"rejected",
                                           "shipment_id"}
     -> 200 OK (any body); this is the human-in-the-loop signal for retraining.

Any failure or timeout falls back to fixtures and the header keeps showing DEMO DATA,
so the dashboard never breaks during a live pitch.
"""

from __future__ import annotations

import os
from typing import Any

import requests
import streamlit as st

import static_data

TIMEOUT = 8


# ------------------------------------------------------------------ transport

def _base_url() -> str:
    """Resolve the agent endpoint from env or Streamlit secrets. Empty means demo mode."""
    url = os.environ.get("CEPH_API_URL", "")
    if not url:
        try:
            url = st.secrets.get("CEPH_API_URL", "")  # type: ignore[assignment]
        except Exception:
            url = ""
    return str(url).rstrip("/")


def is_live() -> bool:
    """True only when an endpoint is configured *and* actually answering.

    Prevents the header claiming "Live agent" while the dashboard is silently
    serving fixtures because the endpoint is down.
    """
    base = _base_url()
    if not base:
        return False
    return _probe(base)


@st.cache_data(ttl=30, show_spinner=False)
def _probe(base: str) -> bool:
    try:
        response = requests.get(f"{base}/shipments", timeout=TIMEOUT)
        return response.ok
    except Exception:
        return False


def _get(path: str) -> Any | None:
    base = _base_url()
    if not base:
        return None
    try:
        response = requests.get(f"{base}{path}", timeout=TIMEOUT)
        response.raise_for_status()
        return response.json()
    except Exception:
        return None


def _post(path: str, payload: dict) -> Any | None:
    base = _base_url()
    if not base:
        return None
    try:
        response = requests.post(f"{base}{path}", json=payload, timeout=TIMEOUT)
        response.raise_for_status()
        return response.json()
    except Exception:
        return None


# ------------------------------------------------------------------ accessors

def list_shipments() -> list[str]:
    data = _get("/shipments")
    if isinstance(data, dict) and data.get("shipments"):
        return list(data["shipments"])
    return list(static_data.SHIPMENTS.keys())


def get_shipment(shipment_id: str) -> dict:
    data = _get(f"/shipments/{shipment_id}")
    if isinstance(data, dict) and data.get("shipment_id"):
        return data
    fixture = static_data.SHIPMENTS.get(shipment_id)
    if fixture is None:
        fixture = next(iter(static_data.SHIPMENTS.values()))
    return {k: v for k, v in fixture.items() if k not in ("routes", "decisions")}


def get_routes(shipment_id: str) -> list[dict]:
    data = _get(f"/shipments/{shipment_id}/routes")
    if isinstance(data, dict) and data.get("routes"):
        return list(data["routes"])
    fixture = static_data.SHIPMENTS.get(shipment_id)
    if fixture is None:
        fixture = next(iter(static_data.SHIPMENTS.values()))
    return list(fixture["routes"])


def get_decisions(shipment_id: str) -> list[dict]:
    data = _get(f"/shipments/{shipment_id}/decisions")
    if isinstance(data, dict) and data.get("decisions"):
        return list(data["decisions"])
    fixture = static_data.SHIPMENTS.get(shipment_id)
    if fixture is None:
        fixture = next(iter(static_data.SHIPMENTS.values()))
    return list(fixture["decisions"])


def get_feed() -> list[dict]:
    data = _get("/ingestion")
    if isinstance(data, dict) and data.get("feed"):
        return list(data["feed"])
    return list(static_data.INGESTION_FEED)


def ask_agent(question: str, shipment_id: str | None = None) -> str:
    """Route a question to the agent; keyword-matched demo answers until it is wired up."""
    data = _post("/chat", {"question": question, "shipment_id": shipment_id})
    if isinstance(data, dict) and data.get("answer"):
        return str(data["answer"])

    lowered = question.lower()
    best, best_hits = None, 0
    for keywords, answer in static_data.CANNED_ANSWERS:
        hits = sum(1 for keyword in keywords if keyword in lowered)
        if hits > best_hits:
            best, best_hits = answer, hits
    return best if best else static_data.FALLBACK_ANSWER


def send_feedback(decision_id: str, verdict: str, shipment_id: str | None = None) -> None:
    """Human-in-the-loop signal. No-op in demo mode; posts to the agent when live."""
    _post("/feedback", {
        "decision_id": decision_id,
        "verdict": verdict,
        "shipment_id": shipment_id,
    })
