"""DSV Ceph AI — logistics decision dashboard.

Run:  streamlit run app.py
"""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

import agent_client as agent
from theme import (
    COLORS,
    OCTOPUS,
    badge,
    confidence_bar,
    esc,
    inject_css,
    kpi,
    kv,
    panel_title,
    plotly_layout,
)

st.set_page_config(
    page_title="DSV Ceph AI",
    page_icon="🐙",
    layout="wide",
    initial_sidebar_state="collapsed",
)
inject_css()

st.session_state.setdefault("chat", [])
st.session_state.setdefault("verdicts", {})


def risk_band(hours: float) -> tuple[str, str, str]:
    """Buffer between ETA and deadline → (label, badge kind, colour token)."""
    if hours < 0:
        return "Past deadline", "critical", "ice"
    if hours < 12:
        return "At risk", "warn", "ice"
    return "On track", "ok", "cyan"


# ----------------------------------------------------------------- top bar

live = agent.is_live()
source_badge = badge("Live agent", "live", dot=True) if live else badge("Demo data", "demo", dot=True)

st.markdown(
    f'<div class="topbar">{OCTOPUS}'
    '<span class="wordmark">DSV <span>Ceph</span> AI</span>'
    '<span class="tagline">One data. Smarter decisions. Better services for you.</span>'
    f"{source_badge}</div>",
    unsafe_allow_html=True,
)

controls = st.columns([2, 2, 4])
with controls[0]:
    shipment_id = st.selectbox("Shipment", agent.list_shipments(), label_visibility="visible")
with controls[1]:
    threshold = st.slider("Auto-decision threshold", 50, 100, 95, 1, format="%d%%")

shipment = agent.get_shipment(shipment_id)
routes = agent.get_routes(shipment_id)
decisions = agent.get_decisions(shipment_id)

baseline = next((r for r in routes if r.get("baseline")), routes[0])
recommended = next(
    (r for r in routes if r["route"] == shipment.get("recommended_route")), routes[0]
)
co2_delta = recommended["co2e_kg"] - baseline["co2e_kg"]
time_gained = recommended["hours_before_deadline"] - baseline["hours_before_deadline"]
pending = [d for d in decisions if d["confidence"] < threshold]
hours_left = float(shipment.get("hours_to_deadline", 0))
risk_label, risk_kind, risk_tone = risk_band(hours_left)

# ----------------------------------------------------------------- kpi strip

tiles = st.columns(6)
kpis = [
    kpi("Shipment", shipment["shipment_id"], shipment["container"], small=True, accent=True),
    kpi("Customer", shipment["customer"], shipment["cargo"], small=True),
    kpi("Corridor", f'{shipment["origin"].split(",")[0]} → {shipment["destination"].split(",")[0]}',
        " · ".join(shipment.get("legs", [])), small=True),
    kpi("Deadline buffer", f"{hours_left:.0f} h", risk_label, tone=risk_tone),
    kpi("CO2e — recommended",
        f'{recommended["co2e_kg"]:,.0f} kg',
        f'{co2_delta:+,.0f} kg vs booked · {recommended["route"]}',
        tone="cyan" if co2_delta <= 0 else "ice"),
    kpi("Human review", f"{len(pending)}", f"of {len(decisions)} decisions", tone="ice"),
]
for column, tile in zip(tiles, kpis):
    column.markdown(tile, unsafe_allow_html=True)

st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

# ------------------------------------------------- status + decision queue

left, right = st.columns([1, 1.35])

with left:
    body = [panel_title("Live status")]
    body.append(kv("Current location", shipment["current_location"]))
    body.append(kv("Status", shipment["current_status"]))
    body.append(kv("Last tracking event", shipment["latest_tracking"]))
    body.append(kv("Disruption", shipment["disruption"], tone="ice"))
    body.append(kv("Priority", shipment["priority"], tone="ice"))
    body.append(kv("Weight", f'{shipment["weight_kg"]:,} kg'))
    st.markdown(f'<div class="glass">{"".join(body)}</div>', unsafe_allow_html=True)

    risk = [panel_title("Delivery risk")]
    risk.append(kv("Revised ETA", shipment["eta"]))
    risk.append(kv("Delivery deadline", shipment["deadline"]))
    risk.append(kv("Buffer", f"{hours_left:.1f} h", tone=risk_tone))
    risk.append(
        f'<div style="margin-top:10px">{badge(risk_label, risk_kind, dot=True)} '
        f'<span class="kpi-sub" style="margin-left:6px">'
        f'{esc(recommended["route"])} {"recovers" if time_gained >= 0 else "gives up"} '
        f'{abs(time_gained):.0f} h against the booked routing'
        f"</span></div>"
    )
    st.markdown(f'<div class="glass">{"".join(risk)}</div>', unsafe_allow_html=True)

    rows = [panel_title("Layer 1 — data ingestion")]
    status_tone = {"Mapped": "t-cyan", "Needs review": "t-ice", "Parsing": "t-muted"}
    for item in agent.get_feed():
        tone = status_tone.get(item["status"], "t-muted")
        rows.append(
            '<div class="feed-row">'
            f'<span class="chip">{esc(item["format"])}</span>'
            f'<span class="feed-name">{esc(item["name"])}</span>'
            f'<span class="{tone}" style="font-size:11px;min-width:82px;text-align:right">'
            f'{esc(item["status"])}</span>'
            "</div>"
        )
    st.markdown(f'<div class="glass">{"".join(rows)}</div>', unsafe_allow_html=True)

with right:
    st.markdown(
        f'<div class="panel-title">Decision queue &nbsp;'
        f'{badge(f"threshold {threshold}%", "ai")}</div>',
        unsafe_allow_html=True,
    )
    for decision in decisions:
        auto = decision["confidence"] >= threshold
        state_badge = badge("Auto-approved", "ok") if auto else badge("Human review", "warn")
        verdict = st.session_state["verdicts"].get(decision["id"])

        st.markdown(
            f'<div class="decision">'
            f'<div class="decision-head">'
            f'<span class="decision-title">{esc(decision["title"])}</span>{state_badge}</div>'
            f'{confidence_bar(decision["confidence"])}'
            f'<div class="kpi-sub">{esc(decision["id"])} · {esc(decision["classification"])} · '
            f'{esc(decision["action"])}</div>'
            f"</div>",
            unsafe_allow_html=True,
        )

        with st.expander("Why this decision"):
            # Rationale is model-written free text — the least trustworthy string on
            # the page, so it goes through Streamlit's own markdown list rather than
            # being spliced into HTML.
            for reason in decision["rationale"]:
                st.markdown(f"- {reason}")

        if not auto:
            actions = st.columns([1, 1, 4])
            if actions[0].button("Approve", key=f"ok-{decision['id']}"):
                st.session_state["verdicts"][decision["id"]] = "approved"
                agent.send_feedback(decision["id"], "approved", shipment_id)
                st.rerun()
            if actions[1].button("Reject", key=f"no-{decision['id']}"):
                st.session_state["verdicts"][decision["id"]] = "rejected"
                agent.send_feedback(decision["id"], "rejected", shipment_id)
                st.rerun()
            if verdict:
                actions[2].markdown(
                    f'<div style="padding-top:4px">'
                    f'{badge(f"{verdict} — fed back to model", "ai")}</div>',
                    unsafe_allow_html=True,
                )

# ----------------------------------------------------------------- charts

frame = pd.DataFrame(routes)
names = frame["route"].tolist()
highlight = shipment.get("recommended_route")

# One rule for both charts so a route keeps its identity across them:
# ice = the recommendation, dark = the booked baseline, mid blue = other candidates.
# Routes that arrive after the deadline are outlined instead of filled — disqualified.
bar_colors = [
    COLORS["ice"] if name == highlight else
    (COLORS["deep"] if row_baseline else COLORS["blue"])
    for name, row_baseline in zip(names, frame["baseline"])
]
disqualified = [hours < 0 for hours in frame["hours_before_deadline"]]
outline_colors = [COLORS["ice"] if late else "rgba(0,0,0,0)" for late in disqualified]
bar_fills = [
    COLORS["bg"] if late else color for late, color in zip(disqualified, bar_colors)
]
marker_line = dict(color=outline_colors, width=1.4)

chart_left, chart_right = st.columns(2)

with chart_left:
    st.markdown(panel_title("Estimated CO2e by route (kg)"), unsafe_allow_html=True)
    fig = go.Figure(
        go.Bar(
            x=names,
            y=frame["co2e_kg"],
            marker_color=bar_fills,
            marker_line=marker_line,
            text=[f"{value:,.0f}" for value in frame["co2e_kg"]],
            textposition="outside",
            textfont=dict(size=11, color=COLORS["muted"]),
            customdata=frame[["label", "modes"]].values,
            hovertemplate="<b>%{x}</b><br>%{customdata[0]}<br>%{customdata[1]}"
                          "<br>%{y:,.0f} kg CO2e<extra></extra>",
        )
    )
    fig.add_hline(
        y=baseline["co2e_kg"],
        line_dash="dot",
        line_color="rgba(185,214,242,0.30)",
        annotation_text="baseline",
        annotation_position="top left",
        annotation_font=dict(size=10, color=COLORS["muted"]),
    )
    st.plotly_chart(plotly_layout(fig, ytitle="kg CO2e"), width="stretch")

with chart_right:
    st.markdown(panel_title("Hours before deadline by route"), unsafe_allow_html=True)
    fig2 = go.Figure(
        go.Bar(
            x=names,
            y=frame["hours_before_deadline"],
            marker_color=bar_fills,
            marker_line=marker_line,
            text=[f"{value:,.0f} h" for value in frame["hours_before_deadline"]],
            textposition="outside",
            textfont=dict(size=11, color=COLORS["muted"]),
            customdata=frame[["transit_hours"]].values,
            hovertemplate="<b>%{x}</b><br>%{customdata[0]:,.0f} h transit"
                          "<br>%{y:,.1f} h buffer<extra></extra>",
        )
    )
    fig2.add_hline(y=0, line_color="rgba(185,214,242,0.45)", line_width=1)
    st.plotly_chart(plotly_layout(fig2, ytitle="hours"), width="stretch")

# -------------------------------------------------- comparison table + chat

table_col, chat_col = st.columns([1.35, 1])

with table_col:
    st.markdown(panel_title("Route comparison"), unsafe_allow_html=True)
    table = frame.assign(
        Route=frame["route"],
        Option=frame["label"],
        Modes=frame["modes"],
        **{
            "CO2e (kg)": frame["co2e_kg"],
            "Transit (h)": frame["transit_hours"],
            "Buffer (h)": frame["hours_before_deadline"],
            "Cost (EUR)": frame["cost_eur"],
        },
    )[["Route", "Option", "Modes", "CO2e (kg)", "Transit (h)", "Buffer (h)", "Cost (EUR)"]]
    st.dataframe(table, width="stretch", hide_index=True)

with chat_col:
    st.markdown(panel_title("Ask Ceph"), unsafe_allow_html=True)
    if not st.session_state["chat"]:
        st.markdown(
            '<div class="kpi-sub" style="margin:-4px 0 8px 2px">'
            "Try: “why the reroute?” · “compare emissions” · “what needs my approval?”</div>",
            unsafe_allow_html=True,
        )
    for role, message in st.session_state["chat"]:
        with st.chat_message(role):
            st.markdown(message)

    question = st.chat_input("Ask about this shipment…")
    if question:
        st.session_state["chat"].append(("user", question))
        st.session_state["chat"].append(("assistant", agent.ask_agent(question, shipment_id)))
        st.rerun()

st.markdown(
    '<div class="kpi-sub" style="margin-top:18px;padding-top:10px;'
    'border-top:1px solid rgba(185,214,242,0.14)">'
    "Layer 1 ingestion · Layer 2 confidence engine · Layer 3 decision router — "
    f'{"connected to the live Ceph agent" if live else "demo fixtures, agent endpoint not yet connected"}'
    "</div>",
    unsafe_allow_html=True,
)
