"""Design system for the DSV Ceph AI dashboard.

Night operations-centre palette: deep navy base, warm amber accents, teal for data,
muted purple for anything ML-driven. Everything visual is defined here so the rest of
the app only composes layout.
"""

from __future__ import annotations

import streamlit as st

COLORS = {
    "bg": "#0a0e1a",
    "bg_alt": "#111827",
    "card": "#1f2937",
    "amber": "#f59e0b",
    "teal": "#14b8a6",
    "purple": "#7c3aed",
    "orange": "#ea580c",
    "red": "#ef4444",
    "text": "#f3f4f6",
    "muted": "#9ca3af",
    "line": "rgba(255,255,255,0.06)",
    "grid": "rgba(255,255,255,0.05)",
}

CHART_SEQUENCE = [COLORS["amber"], COLORS["teal"], COLORS["orange"], COLORS["purple"]]

STATUS_COLORS = {
    "ok": COLORS["teal"],
    "warn": COLORS["amber"],
    "critical": COLORS["red"],
    "ai": COLORS["purple"],
}

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"], .stApp, button, input, textarea, select {
    font-family: 'Inter', -apple-system, 'Segoe UI', system-ui, sans-serif !important;
}

.stApp {
    background: linear-gradient(160deg, #0a0e1a 0%, #0b1020 45%, #111827 100%);
    background-attachment: fixed;
    color: #f3f4f6;
}

.block-container {
    padding: 1.4rem 2.2rem 3rem 2.2rem !important;
    max-width: 1500px;
}

#MainMenu, footer, header[data-testid="stHeader"] { visibility: hidden; height: 0; }
[data-testid="stDecoration"] { display: none; }
[data-testid="stSidebar"] { display: none; }

h1, h2, h3, h4 { color: #f3f4f6; letter-spacing: -0.015em; font-weight: 600; }

/* ---------- surfaces ---------- */
.glass {
    background: rgba(31, 41, 55, 0.30);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 10px;
    padding: 14px 16px;
    margin-bottom: 12px;
}

.panel-title {
    font-size: 10.5px;
    font-weight: 600;
    letter-spacing: 0.13em;
    text-transform: uppercase;
    color: #9ca3af;
    margin: 0 0 12px 0;
    display: flex;
    align-items: center;
    gap: 8px;
}
.panel-title::after {
    content: "";
    flex: 1;
    height: 1px;
    background: rgba(255,255,255,0.06);
}

/* ---------- top bar ---------- */
.topbar {
    display: flex;
    align-items: baseline;
    gap: 14px;
    padding: 2px 0 14px 0;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    margin-bottom: 16px;
}
.wordmark {
    font-size: 19px;
    font-weight: 700;
    letter-spacing: -0.02em;
    color: #f3f4f6;
}
.wordmark span { color: #f59e0b; }
.tagline {
    font-size: 12px;
    color: #9ca3af;
    flex: 1;
}
.mono { font-variant-numeric: tabular-nums; font-feature-settings: "tnum"; }

/* ---------- badges ---------- */
.badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.09em;
    text-transform: uppercase;
    padding: 3px 9px;
    border-radius: 4px;
    border: 1px solid;
    white-space: nowrap;
}
.badge-demo   { color: #f59e0b; border-color: rgba(245,158,11,0.35); background: rgba(245,158,11,0.08); }
.badge-live   { color: #14b8a6; border-color: rgba(20,184,166,0.35); background: rgba(20,184,166,0.08); }
.badge-ok     { color: #14b8a6; border-color: rgba(20,184,166,0.35); background: rgba(20,184,166,0.08); }
.badge-warn   { color: #f59e0b; border-color: rgba(245,158,11,0.35); background: rgba(245,158,11,0.08); }
.badge-critical { color: #ef4444; border-color: rgba(239,68,68,0.38); background: rgba(239,68,68,0.09); }
.badge-ai     { color: #a78bfa; border-color: rgba(124,58,237,0.42); background: rgba(124,58,237,0.12); }
.dot { width: 6px; height: 6px; border-radius: 50%; background: currentColor; }

/* ---------- kpi tiles ---------- */
.kpi {
    background: rgba(31, 41, 55, 0.30);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 10px;
    padding: 12px 14px;
    height: 100%;
    display: flex;
    flex-direction: column;
}
/* only equalise tile heights once the columns actually sit side by side */
@media (min-width: 640px) {
    .kpi { min-height: 94px; }
    .kpi .kpi-sub { margin-top: auto; padding-top: 4px; }
}
.kpi-accent { box-shadow: 0 0 0 1px rgba(245,158,11,0.18), 0 6px 22px -12px rgba(245,158,11,0.55); }
.kpi-label {
    font-size: 10px;
    letter-spacing: 0.11em;
    text-transform: uppercase;
    color: #9ca3af;
    margin-bottom: 6px;
}
.kpi-value {
    font-size: 20px;
    font-weight: 600;
    color: #f3f4f6;
    line-height: 1.15;
    font-variant-numeric: tabular-nums;
}
.kpi-value.sm { font-size: 15px; }
.kpi-sub { font-size: 11px; color: #9ca3af; margin-top: 4px; }
.t-amber { color: #f59e0b !important; }
.t-teal  { color: #14b8a6 !important; }
.t-purple{ color: #a78bfa !important; }
.t-red   { color: #ef4444 !important; }
.t-muted { color: #9ca3af !important; }

/* ---------- key/value rows ---------- */
.kv { display: flex; justify-content: space-between; gap: 16px; padding: 6px 0; border-bottom: 1px dashed rgba(255,255,255,0.05); }
.kv:last-child { border-bottom: none; }
.kv-k { font-size: 11.5px; color: #9ca3af; }
.kv-v { font-size: 12.5px; color: #f3f4f6; font-weight: 500; text-align: right; font-variant-numeric: tabular-nums; }

/* ---------- decisions ---------- */
.decision {
    border: 1px solid rgba(255,255,255,0.06);
    border-left: 2px solid #7c3aed;
    border-radius: 8px;
    padding: 10px 12px;
    margin-bottom: 9px;
    background: rgba(17,24,39,0.35);
}
.decision-head { display: flex; justify-content: space-between; align-items: center; gap: 10px; margin-bottom: 8px; }
.decision-title { font-size: 12.5px; font-weight: 600; color: #f3f4f6; }
.conf-row { display: flex; align-items: center; gap: 9px; }
.conf-track { flex: 1; height: 4px; border-radius: 2px; background: rgba(255,255,255,0.07); overflow: hidden; }
.conf-fill { height: 100%; border-radius: 2px; }
.conf-num { font-size: 12px; font-weight: 600; font-variant-numeric: tabular-nums; min-width: 46px; text-align: right; }
.rationale { font-size: 11.5px; color: #9ca3af; line-height: 1.65; margin: 8px 0 0 0; padding-left: 14px; }
.rationale li { margin-bottom: 2px; }

/* ---------- feed ---------- */
.feed-row { display: flex; align-items: center; gap: 10px; padding: 7px 0; border-bottom: 1px solid rgba(255,255,255,0.04); font-size: 11.5px; }
.feed-row:last-child { border-bottom: none; }
.chip { font-size: 9.5px; font-weight: 700; letter-spacing: 0.06em; padding: 2px 6px; border-radius: 3px; background: rgba(255,255,255,0.06); color: #9ca3af; min-width: 40px; text-align: center; }
.feed-name { flex: 1; color: #f3f4f6; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.feed-src { color: #9ca3af; font-size: 11px; }

/* ---------- streamlit widget overrides ---------- */
div[data-testid="stSelectbox"] label, div[data-testid="stSlider"] label {
    font-size: 10px !important;
    letter-spacing: 0.11em;
    text-transform: uppercase;
    color: #9ca3af !important;
    font-weight: 600 !important;
}
div[data-baseweb="select"] > div {
    background: rgba(31,41,55,0.45) !important;
    border-color: rgba(255,255,255,0.08) !important;
    font-size: 13px;
}
.stSlider [data-baseweb="slider"] { padding-top: 4px; }

.stButton > button {
    background: rgba(31,41,55,0.45);
    border: 1px solid rgba(255,255,255,0.08);
    color: #f3f4f6;
    font-size: 11.5px;
    font-weight: 500;
    padding: 3px 12px;
    border-radius: 6px;
    min-height: 0;
    transition: border-color .15s ease, color .15s ease;
}
.stButton > button:hover { border-color: rgba(245,158,11,0.5); color: #f59e0b; }
.stButton > button:focus:not(:active) { color: #f59e0b; border-color: rgba(245,158,11,0.5); }

div[data-testid="stExpander"] {
    border: none !important;
    background: transparent !important;
}
div[data-testid="stExpander"] details { border: none !important; background: transparent !important; }
div[data-testid="stExpander"] summary { font-size: 11px !important; color: #9ca3af !important; padding: 2px 0 !important; }
div[data-testid="stExpander"] summary:hover { color: #f59e0b !important; }

div[data-testid="stChatInput"] textarea { font-size: 13px; }
div[data-testid="stChatInput"] > div {
    background: rgba(31,41,55,0.45) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
}
div[data-testid="stChatMessage"] {
    background: rgba(31,41,55,0.28);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 8px;
    padding: 8px 12px;
    margin-bottom: 7px;
}
div[data-testid="stChatMessage"] p { font-size: 12.5px; line-height: 1.6; margin-bottom: 4px; }
div[data-testid="stChatMessageAvatarUser"] {
    background: rgba(245,158,11,0.14) !important;
    color: #f59e0b !important;
    border: 1px solid rgba(245,158,11,0.3);
}
div[data-testid="stChatMessageAvatarAssistant"] {
    background: rgba(124,58,237,0.16) !important;
    color: #a78bfa !important;
    border: 1px solid rgba(124,58,237,0.35);
}

div[data-testid="stDataFrame"] { border: 1px solid rgba(255,255,255,0.06); border-radius: 8px; }

hr { border-color: rgba(255,255,255,0.06); margin: 6px 0 14px 0; }

/* tighten default vertical rhythm for a denser board */
div[data-testid="stVerticalBlock"] > div { gap: 0.35rem; }
</style>
"""


def inject_css() -> None:
    """Load fonts and the full stylesheet. Call once, first thing in app.py."""
    st.markdown(_CSS, unsafe_allow_html=True)


def plotly_layout(fig, height: int = 250, ytitle: str = "", showlegend: bool = False):
    """Apply the shared chart treatment: transparent surface, hairline grid, dense type."""
    fig.update_layout(
        template="plotly_dark",
        height=height,
        margin=dict(l=8, r=8, t=8, b=8),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", size=11.5, color=COLORS["muted"]),
        showlegend=showlegend,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.0,
            x=0,
            font=dict(size=10.5),
            bgcolor="rgba(0,0,0,0)",
        ),
        bargap=0.45,
        hoverlabel=dict(
            bgcolor=COLORS["bg_alt"],
            bordercolor=COLORS["line"],
            font=dict(family="Inter, sans-serif", size=11.5, color=COLORS["text"]),
        ),
    )
    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        linecolor=COLORS["grid"],
        tickfont=dict(size=11, color=COLORS["muted"]),
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor=COLORS["grid"],
        zeroline=False,
        linecolor="rgba(0,0,0,0)",
        title=dict(text=ytitle, font=dict(size=10.5, color=COLORS["muted"])),
        tickfont=dict(size=11, color=COLORS["muted"]),
    )
    return fig


# ---------------------------------------------------------------- html helpers

def panel_title(text: str) -> str:
    return f'<div class="panel-title">{text}</div>'


def badge(text: str, kind: str = "ok", dot: bool = False) -> str:
    marker = '<span class="dot"></span>' if dot else ""
    return f'<span class="badge badge-{kind}">{marker}{text}</span>'


def kpi(label: str, value: str, sub: str = "", tone: str = "", accent: bool = False,
        small: bool = False) -> str:
    tone_cls = f" t-{tone}" if tone else ""
    size_cls = " sm" if small else ""
    accent_cls = " kpi-accent" if accent else ""
    sub_html = f'<div class="kpi-sub">{sub}</div>' if sub else ""
    return (
        f'<div class="kpi{accent_cls}">'
        f'<div class="kpi-label">{label}</div>'
        f'<div class="kpi-value{size_cls}{tone_cls}">{value}</div>'
        f"{sub_html}</div>"
    )


def kv(key: str, value: str, tone: str = "") -> str:
    tone_cls = f" t-{tone}" if tone else ""
    return f'<div class="kv"><span class="kv-k">{key}</span><span class="kv-v{tone_cls}">{value}</span></div>'


def confidence_bar(score: float) -> str:
    """Purple confidence meter — the ML signal always reads purple."""
    pct = max(0.0, min(100.0, score))
    color = COLORS["purple"] if pct >= 60 else COLORS["amber"]
    return (
        '<div class="conf-row">'
        f'<div class="conf-track"><div class="conf-fill" style="width:{pct:.0f}%;'
        f'background:linear-gradient(90deg,{color},#a78bfa);"></div></div>'
        f'<span class="conf-num" style="color:{color}">{pct:.1f}%</span>'
        "</div>"
    )
