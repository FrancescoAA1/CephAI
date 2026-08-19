"""Static demo fixtures.

Mirrors the shape of the payloads Didier's LangChain agent will return, so switching
to the live API is a transport change only. Nothing outside agent_client.py should
import this module.
"""

from __future__ import annotations

SHIPMENTS = {
    "CN-SZ-TR-5567": {
        "shipment_id": "CN-SZ-TR-5567",
        "container": "MSCU7654321",
        "customer": "EuroTech Manufacturing",
        "origin": "Shenzhen, CN",
        "destination": "Rotterdam, NL",
        "cargo": "Industrial control modules",
        "weight_kg": 14800,
        "priority": "Urgent",
        "deadline": "2026-09-03 17:00 CEST",
        "current_location": "Wanliang holding anchorage",
        "current_status": "Awaiting next sailing",
        "latest_tracking": "2026-08-27 03:30 CST",
        "disruption": "Typhoon Kirogi — widespread port congestion",
        "eta": "2026-09-01 23:00 CEST",
        "hours_to_deadline": 42.0,
        "legs": ["Sea", "Rail", "Road"],
        "baseline_route": "Qinhuai",
        "recommended_route": "ROUTE-B",
        "routes": [
            {
                "route": "Qinhuai",
                "label": "Baseline (booked)",
                "co2e_kg": 1200,
                "transit_hours": 185,
                "hours_before_deadline": 11,
                "cost_eur": 8450,
                "modes": "Sea → Road",
                "baseline": True,
            },
            {
                "route": "ROUTE-A",
                "label": "Air bridge via Frankfurt",
                "co2e_kg": 1400,
                "transit_hours": 144,
                "hours_before_deadline": 52,
                "cost_eur": 19200,
                "modes": "Sea → Air → Road",
                "baseline": False,
            },
            {
                "route": "ROUTE-B",
                "label": "Rail corridor via Duisburg",
                "co2e_kg": 1300,
                "transit_hours": 154,
                "hours_before_deadline": 42,
                "cost_eur": 10650,
                "modes": "Sea → Rail → Road",
                "baseline": False,
            },
            {
                "route": "ROUTE-C",
                "label": "Transshipment via Singapore",
                "co2e_kg": 1500,
                "transit_hours": 200,
                "hours_before_deadline": -4,
                "cost_eur": 9100,
                "modes": "Sea → Sea → Road",
                "baseline": False,
            },
        ],
        "decisions": [
            {
                "id": "DEC-4471",
                "title": "Re-route via ROUTE-B (rail corridor, Duisburg)",
                "confidence": 96.4,
                "classification": "Operational",
                "action": "Rebook rail leg, release container at Yantian",
                "rationale": [
                    "Typhoon Kirogi closes Yantian outbound berths for an estimated 62 h.",
                    "Booked Qinhuai routing falls to an 11 h buffer — inside the at-risk band.",
                    "ROUTE-B restores a 42 h buffer, recovering 31 h against the booked plan.",
                    "The air bridge buys 10 h more slack but costs €8,550 extra and 100 kg more CO2e.",
                    "Carrier confirmed rail slot availability in the 29 Aug departure window.",
                ],
            },
            {
                "id": "DEC-4472",
                "title": "Auto-map partner manifest to DSV schema",
                "confidence": 98.9,
                "classification": "Non-confidential",
                "action": "Ingest Schmitz Cargobull CSV → unified shipment record",
                "rationale": [
                    "All 24 columns matched known field aliases with exact type agreement.",
                    "Container and booking references reconcile against the TMS record.",
                    "Format signature seen 1,842 times previously with a 0.3% correction rate.",
                ],
            },
            {
                "id": "DEC-4473",
                "title": "Release customs value to Arla shared view",
                "confidence": 71.2,
                "classification": "Confidential — commercial terms",
                "action": "Publish declared value and HS codes to the partner portal",
                "rationale": [
                    "Document contains declared commercial value; classifier flags it confidential.",
                    "Customer agreement on value-sharing could not be verified automatically.",
                    "Below threshold — routed for human approval before any disclosure.",
                ],
            },
            {
                "id": "DEC-4474",
                "title": "Notify consignee of revised ETA",
                "confidence": 93.1,
                "classification": "Operational",
                "action": "Send revised ETA 2026-09-01 23:00 to EuroTech Manufacturing",
                "rationale": [
                    "Revised ETA derived from the ROUTE-B booking, still pending final confirmation.",
                    "Consignee has an SLA requiring notice within 4 h of any deadline change.",
                    "Confidence held below threshold until the carrier slot is confirmed.",
                ],
            },
        ],
    },
    "DK-AAR-RD-2210": {
        "shipment_id": "DK-AAR-RD-2210",
        "container": "TRLU4419087",
        "customer": "Arla Foods",
        "origin": "Aarhus, DK",
        "destination": "Hamburg, DE",
        "cargo": "Chilled dairy (2–6 °C)",
        "weight_kg": 21400,
        "priority": "Temperature critical",
        "deadline": "2026-08-28 06:00 CEST",
        "current_location": "Padborg border crossing",
        "current_status": "In transit — customs cleared",
        "latest_tracking": "2026-08-27 04:10 CEST",
        "disruption": "A7 lane closure north of Flensburg",
        "eta": "2026-08-28 00:35 CEST",
        "hours_to_deadline": 5.4,
        "legs": ["Road"],
        "baseline_route": "RD-DIRECT",
        "recommended_route": "RD-B7",
        "routes": [
            {
                "route": "RD-DIRECT",
                "label": "Baseline (booked)",
                "co2e_kg": 410,
                "transit_hours": 9.1,
                "hours_before_deadline": 1.8,
                "cost_eur": 1180,
                "modes": "Road",
                "baseline": True,
            },
            {
                "route": "RD-B7",
                "label": "B7 coastal diversion",
                "co2e_kg": 445,
                "transit_hours": 5.5,
                "hours_before_deadline": 5.4,
                "cost_eur": 1290,
                "modes": "Road",
                "baseline": False,
            },
            {
                "route": "RD-RAIL",
                "label": "Rail shuttle via Flensburg",
                "co2e_kg": 195,
                "transit_hours": 12.1,
                "hours_before_deadline": -1.2,
                "cost_eur": 980,
                "modes": "Road → Rail",
                "baseline": False,
            },
        ],
        "decisions": [
            {
                "id": "DEC-4480",
                "title": "Divert to B7 coastal route",
                "confidence": 97.8,
                "classification": "Operational",
                "action": "Push new routing to the driver's device",
                "rationale": [
                    "A7 closure adds an estimated 96 min; cold-chain buffer falls under 2 h.",
                    "B7 restores a 5.4 h buffer for a 35 kg CO2e penalty.",
                    "Reefer fuel reserve is sufficient for the longer surface distance.",
                ],
            },
            {
                "id": "DEC-4481",
                "title": "Reject rail shuttle alternative",
                "confidence": 99.1,
                "classification": "Operational",
                "action": "Discard RD-RAIL from candidate set",
                "rationale": [
                    "Arrival lands 1.2 h after the delivery deadline.",
                    "Lowest emissions in the set, but the temperature SLA is binding.",
                ],
            },
            {
                "id": "DEC-4482",
                "title": "Share temperature log with Arla quality team",
                "confidence": 88.4,
                "classification": "Confidential — quality data",
                "action": "Publish reefer telemetry for the last 12 h",
                "rationale": [
                    "Telemetry includes a 4-minute excursion to 6.4 °C at the border stop.",
                    "Excursion is within tolerance but requires a human sign-off before release.",
                ],
            },
        ],
    },
}

INGESTION_FEED = [
    {"format": "CSV", "name": "schmitz_manifest_2026-08-27.csv", "source": "Schmitz Cargobull", "status": "Mapped", "records": 24},
    {"format": "PDF", "name": "customs_decl_MSCU7654321.pdf", "source": "Yantian Customs Broker", "status": "Needs review", "records": 1},
    {"format": "JSON", "name": "tms_road_eu_delta.json", "source": "DSV TMS #17 (Road EU)", "status": "Mapped", "records": 318},
    {"format": "TXT", "name": "carrier_notice_kirogi.txt", "source": "Maersk Ops Notice", "status": "Mapped", "records": 1},
    {"format": "CSV", "name": "arla_reefer_telemetry.csv", "source": "Arla Foods", "status": "Mapped", "records": 1440},
    {"format": "JSON", "name": "partner_eta_feed_apac.json", "source": "APAC Partner Gateway", "status": "Parsing", "records": 87},
]

CANNED_ANSWERS = [
    (
        ["status", "where", "location", "5567"],
        "**CN-SZ-TR-5567** is held at Wanliang anchorage, awaiting the next sailing after "
        "Typhoon Kirogi closed outbound berths at Yantian. Last position update 2026-08-27 03:30 CST. "
        "Revised ETA Rotterdam 2026-09-01 23:00 CEST — 42 h before the delivery deadline, on the "
        "recommended ROUTE-B rail corridor.",
    ),
    (
        ["co2", "emission", "carbon", "sustainab"],
        "Across the four candidate routes, CO2e ranges from 1,200 kg (Qinhuai baseline) to 1,500 kg "
        "(ROUTE-C via Singapore). The recommended **ROUTE-B** rail corridor lands at 1,300 kg — "
        "100 kg above the booked routing, which no longer makes the deadline, and 100 kg below the "
        "air bridge that does.",
    ),
    (
        ["route", "reroute", "divert", "alternative", "recommend"],
        "Recommendation: **ROUTE-B — rail corridor via Duisburg**, confidence **96.4%** (auto-approved). "
        "It restores a 42 h buffer against 11 h on the booked routing, at €10,650 — roughly 55% of "
        "the air-bridge cost and 100 kg CO2e lighter.",
    ),
    (
        ["eta", "deadline", "late", "delay", "risk"],
        "ETA is 2026-09-01 23:00 CEST against a 2026-09-03 17:00 CEST deadline — a 42 h buffer, "
        "classified **on track**. The booked Qinhuai routing would have left 11 h, inside the "
        "at-risk band, and the Singapore transshipment arrives 4 h late.",
    ),
    (
        ["confiden", "why", "explain", "score"],
        "Confidence is produced by the Layer-2 classifier from format match quality, historical "
        "correction rate, and how well the source reconciles against the TMS record. Anything at or "
        "above the routing threshold executes automatically; everything below it queues for a human, "
        "and that verdict is fed back into the model.",
    ),
    (
        ["confidential", "sensitive", "gdpr", "privacy"],
        "One item is flagged confidential: **DEC-4473**, release of declared customs value and HS codes "
        "to the Arla shared view, at 71.2% confidence. Commercial-terms data always requires human "
        "approval before disclosure, regardless of score.",
    ),
    (
        ["arla", "2210", "dairy", "reefer", "temperature"],
        "**DK-AAR-RD-2210** (Arla chilled dairy) is at the Padborg crossing, customs cleared. The A7 "
        "closure north of Flensburg cut the cold-chain buffer below 2 h, so the B7 coastal diversion "
        "was auto-approved at 97.8%, restoring a 5.4 h buffer.",
    ),
    (
        ["file", "format", "csv", "json", "pdf", "ingest", "upload"],
        "Layer 1 has taken in 6 files in this window — CSV, JSON, PDF and TXT — from Schmitz Cargobull, "
        "Arla, a customs broker, a carrier notice and two DSV TMS instances. Five are mapped to the "
        "unified schema; the customs PDF is held for review.",
    ),
]

FALLBACK_ANSWER = (
    "Running on demo data, so I can answer on the two loaded shipments — status and delivery risk, "
    "route and emissions comparison, confidence scores and decision rationale, or what Layer 1 has "
    "ingested. Once the live endpoint is connected the same questions hit the full agent."
)
