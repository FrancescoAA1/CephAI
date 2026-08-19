"""Design system for the DSV Ceph AI dashboard.

Palette: https://coolors.co/palette/b9d6f2-061a40-0353a4-006daa-003559
Deep navy ground, three blues for data, ice blue for anything that needs the eye.
Square corners throughout, no motion, no glow.
"""

from __future__ import annotations

import html

import streamlit as st

COLORS = {
    "bg": "#061a40",
    "deep": "#003559",
    "blue": "#0353a4",
    "cyan": "#006daa",
    "ice": "#b9d6f2",
    "text": "#b9d6f2",
    "muted": "#7a9cc6",
    "line": "rgba(185,214,242,0.14)",
    "grid": "rgba(185,214,242,0.07)",
}

CHART_SEQUENCE = [COLORS["ice"], COLORS["cyan"], COLORS["blue"], COLORS["deep"]]

STATUS_COLORS = {
    "ok": COLORS["cyan"],
    "warn": COLORS["ice"],
    "critical": COLORS["ice"],
}

OCTOPUS = """
<svg class="octo" width="30" height="30" viewBox="0 0 32 32" fill="none">
  <path d="M16 3.2c-5.6 0-9.2 3.9-9.2 9 0 2.9.7 5.1 1.5 6.7h15.4c.8-1.6 1.5-3.8 1.5-6.7
           0-5.1-3.6-9-9.2-9z" fill="#b9d6f2"/>
  <circle cx="12.7" cy="11.9" r="1.6" fill="#061a40"/>
  <circle cx="19.3" cy="11.9" r="1.6" fill="#061a40"/>
  <g stroke="#b9d6f2" stroke-width="2" stroke-linecap="round">
    <path d="M7.6 19.2c-.9 3.2-2.6 5.4-5 6.5-1.2.5-1.9-.9-.6-1.5"/>
    <path d="M11.7 19.6c-.6 3.8-1.5 6.6-2.6 8.3-.7 1.1-2 .3-1.4-1"/>
    <path d="M16 19.8c.3 3.9.2 6.9-.3 8.9-.3 1.3-1.8 1-1.5-.4"/>
    <path d="M20.3 19.6c.6 3.8 1.5 6.6 2.6 8.3.7 1.1 2 .3 1.4-1"/>
    <path d="M24.4 19.2c.9 3.2 2.6 5.4 5 6.5 1.2.5 1.9-.9.6-1.5"/>
  </g>
</svg>
"""

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"], .stApp, button, input, textarea, select {
    font-family: 'Inter', -apple-system, 'Segoe UI', system-ui, sans-serif !important;
}

.stApp {
    background: #061a40;
    color: #b9d6f2;
}

.block-container {
    padding: 1.4rem 2.2rem 3rem 2.2rem !important;
    max-width: 1500px;
}

#MainMenu, footer, header[data-testid="stHeader"] { visibility: hidden; height: 0; }
[data-testid="stDecoration"] { display: none; }
[data-testid="stSidebar"] { display: none; }

/* square everything, kill all motion */
*, *::before, *::after {
    border-radius: 0 !important;
    transition: none !important;
    animation: none !important;
    box-shadow: none !important;
}

h1, h2, h3, h4 { color: #b9d6f2; letter-spacing: -0.015em; font-weight: 600; }

/* ---------- surfaces ---------- */
.glass {
    background: #003559;
    border: 1px solid rgba(185,214,242,0.14);
    padding: 14px 16px;
    margin-bottom: 12px;
}

.panel-title {
    font-size: 10.5px;
    font-weight: 600;
    letter-spacing: 0.13em;
    text-transform: uppercase;
    color: #7a9cc6;
    margin: 0 0 12px 0;
    display: flex;
    align-items: center;
    gap: 8px;
}
.panel-title::after {
    content: "";
    flex: 1;
    height: 1px;
    background: rgba(185,214,242,0.14);
}

/* ---------- top bar ---------- */
.topbar {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 2px 0 14px 0;
    border-bottom: 1px solid rgba(185,214,242,0.14);
    margin-bottom: 16px;
}
.octo { flex: none; display: block; }
.wordmark {
    font-size: 19px;
    font-weight: 700;
    letter-spacing: -0.02em;
    color: #7a9cc6;
}
.wordmark span { color: #b9d6f2; }
.tagline {
    font-size: 12px;
    color: #7a9cc6;
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
    border: 1px solid;
    white-space: nowrap;
}
.badge-demo { color: #b9d6f2; border-color: rgba(185,214,242,0.45); background: transparent; }
.badge-live { color: #061a40; border-color: #006daa; background: #006daa; }
.badge-ok   { color: #b9d6f2; border-color: #006daa; background: transparent; }
.badge-warn { color: #b9d6f2; border-color: rgba(185,214,242,0.55); background: transparent; }
/* loudest treatment available inside the palette: full ice fill on navy */
.badge-critical { color: #061a40; border-color: #b9d6f2; background: #b9d6f2; }
.badge-ai   { color: #b9d6f2; border-color: #0353a4; background: #0353a4; }
.dot { width: 6px; height: 6px; background: currentColor; }

/* ---------- kpi tiles ---------- */
.kpi {
    background: #003559;
    border: 1px solid rgba(185,214,242,0.14);
    padding: 12px 14px;
    height: 100%;
    display: flex;
    flex-direction: column;
}
@media (min-width: 640px) {
    .kpi { min-height: 94px; }
    .kpi .kpi-sub { margin-top: auto; padding-top: 4px; }
}
.kpi-accent { border-left: 3px solid #b9d6f2; }
.kpi-label {
    font-size: 10px;
    letter-spacing: 0.11em;
    text-transform: uppercase;
    color: #7a9cc6;
    margin-bottom: 6px;
}
.kpi-value {
    font-size: 20px;
    font-weight: 600;
    color: #b9d6f2;
    line-height: 1.15;
    font-variant-numeric: tabular-nums;
}
.kpi-value.sm { font-size: 15px; }
.kpi-sub { font-size: 11px; color: #7a9cc6; margin-top: 4px; }
.t-ice   { color: #b9d6f2 !important; }
.t-cyan  { color: #006daa !important; }
.t-blue  { color: #0353a4 !important; }
.t-muted { color: #7a9cc6 !important; }

/* ---------- key/value rows ---------- */
.kv { display: flex; justify-content: space-between; gap: 16px; padding: 6px 0; border-bottom: 1px solid rgba(185,214,242,0.07); }
.kv:last-child { border-bottom: none; }
.kv-k { font-size: 11.5px; color: #7a9cc6; }
.kv-v { font-size: 12.5px; color: #b9d6f2; font-weight: 500; text-align: right; font-variant-numeric: tabular-nums; }

/* ---------- decisions ---------- */
.decision {
    border: 1px solid rgba(185,214,242,0.14);
    border-left: 3px solid #0353a4;
    padding: 10px 12px;
    margin-bottom: 9px;
    background: #003559;
}
.decision-head { display: flex; justify-content: space-between; align-items: center; gap: 10px; margin-bottom: 8px; }
.decision-title { font-size: 12.5px; font-weight: 600; color: #b9d6f2; }
.conf-row { display: flex; align-items: center; gap: 9px; }
.conf-track { flex: 1; height: 4px; background: rgba(185,214,242,0.12); overflow: hidden; }
.conf-fill { height: 100%; }
.conf-num { font-size: 12px; font-weight: 600; font-variant-numeric: tabular-nums; min-width: 46px; text-align: right; }
/* Rationale is rendered as native markdown (never raw HTML — it's model-written
   text), so the expander's own list is styled to match the dense panels. */
[data-testid="stExpander"] [data-testid="stMarkdownContainer"] ul {
    font-size: 11.5px; color: #7a9cc6; line-height: 1.65; margin: 2px 0 0 0; padding-left: 14px;
}
[data-testid="stExpander"] [data-testid="stMarkdownContainer"] li { margin-bottom: 2px; }
[data-testid="stExpander"] [data-testid="stMarkdownContainer"] li p { font-size: 11.5px; margin: 0; }

/* ---------- feed ---------- */
.feed-row { display: flex; align-items: center; gap: 10px; padding: 7px 0; border-bottom: 1px solid rgba(185,214,242,0.07); font-size: 11.5px; }
.feed-row:last-child { border-bottom: none; }
.chip { font-size: 9.5px; font-weight: 700; letter-spacing: 0.06em; padding: 2px 6px; background: #0353a4; color: #b9d6f2; min-width: 40px; text-align: center; }
.feed-name { flex: 1; color: #b9d6f2; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.feed-src { color: #7a9cc6; font-size: 11px; }

/* ---------- streamlit widget overrides ---------- */
div[data-testid="stSelectbox"] label, div[data-testid="stSlider"] label {
    font-size: 10px !important;
    letter-spacing: 0.11em;
    text-transform: uppercase;
    color: #7a9cc6 !important;
    font-weight: 600 !important;
}
div[data-baseweb="select"] > div {
    background: #003559 !important;
    border-color: rgba(185,214,242,0.18) !important;
    font-size: 13px;
}
div[data-baseweb="popover"] li { font-size: 13px; }
.stSlider [data-baseweb="slider"] { padding-top: 4px; }

.stButton > button {
    background: #003559;
    border: 1px solid rgba(185,214,242,0.22);
    color: #b9d6f2;
    font-size: 11.5px;
    font-weight: 500;
    padding: 3px 12px;
    min-height: 0;
}
.stButton > button:hover { border-color: #b9d6f2; color: #b9d6f2; background: #0353a4; }
.stButton > button:focus:not(:active) { color: #b9d6f2; border-color: #b9d6f2; }

div[data-testid="stExpander"] { border: none !important; background: transparent !important; }
div[data-testid="stExpander"] details { border: none !important; background: transparent !important; }
div[data-testid="stExpander"] summary { font-size: 11px !important; color: #7a9cc6 !important; padding: 2px 0 !important; }
div[data-testid="stExpander"] summary:hover { color: #b9d6f2 !important; }

div[data-testid="stChatInput"] textarea { font-size: 13px; }
div[data-testid="stChatInput"] > div {
    background: #003559 !important;
    border: 1px solid rgba(185,214,242,0.18) !important;
}
div[data-testid="stChatMessage"] {
    background: #003559;
    border: 1px solid rgba(185,214,242,0.10);
    padding: 8px 12px;
    margin-bottom: 7px;
}
div[data-testid="stChatMessage"] p { font-size: 12.5px; line-height: 1.6; margin-bottom: 4px; }
div[data-testid="stChatMessageAvatarUser"] {
    background: #0353a4 !important;
    color: #b9d6f2 !important;
    border: 1px solid rgba(185,214,242,0.22);
}
div[data-testid="stChatMessageAvatarAssistant"] {
    background: #006daa !important;
    color: #b9d6f2 !important;
    border: 1px solid rgba(185,214,242,0.22);
}

div[data-testid="stDataFrame"] { border: 1px solid rgba(185,214,242,0.14); }

hr { border-color: rgba(185,214,242,0.14); margin: 6px 0 14px 0; }

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
            bgcolor=COLORS["deep"],
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
#
# Everything below is rendered through st.markdown(unsafe_allow_html=True), which
# Streamlit passes to rehype-raw with no sanitiser. Today the values are local
# fixtures, but once CEPH_API_URL points at the live agent they become partner
# documents and model-written text — i.e. untrusted. So every interpolated value
# is escaped here, at the single boundary, rather than trusting each call site.

_BADGE_KINDS = {"demo", "live", "ok", "warn", "critical", "ai"}
_TONES = {"ice", "cyan", "blue", "muted"}


def esc(value) -> str:
    return html.escape(str(value), quote=True)


def _cls(value: str, allowed: set) -> str:
    """Class-name tokens are allow-listed, not escaped — they land inside an attribute."""
    return value if value in allowed else ""


def panel_title(text: str) -> str:
    return f'<div class="panel-title">{esc(text)}</div>'


def badge(text: str, kind: str = "ok", dot: bool = False) -> str:
    marker = '<span class="dot"></span>' if dot else ""
    return f'<span class="badge badge-{_cls(kind, _BADGE_KINDS)}">{marker}{esc(text)}</span>'


def kpi(label: str, value: str, sub: str = "", tone: str = "", accent: bool = False,
        small: bool = False) -> str:
    tone_cls = f" t-{_cls(tone, _TONES)}" if _cls(tone, _TONES) else ""
    size_cls = " sm" if small else ""
    accent_cls = " kpi-accent" if accent else ""
    sub_html = f'<div class="kpi-sub">{esc(sub)}</div>' if sub else ""
    return (
        f'<div class="kpi{accent_cls}">'
        f'<div class="kpi-label">{esc(label)}</div>'
        f'<div class="kpi-value{size_cls}{tone_cls}">{esc(value)}</div>'
        f"{sub_html}</div>"
    )


def kv(key: str, value: str, tone: str = "") -> str:
    tone_cls = f" t-{_cls(tone, _TONES)}" if _cls(tone, _TONES) else ""
    return (
        f'<div class="kv"><span class="kv-k">{esc(key)}</span>'
        f'<span class="kv-v{tone_cls}">{esc(value)}</span></div>'
    )


def confidence_bar(score: float) -> str:
    """Confidence meter — ice for high certainty, mid blue when the model is unsure."""
    try:
        pct = float(score)
    except (TypeError, ValueError):
        pct = 0.0
    pct = max(0.0, min(100.0, pct))
    color = COLORS["ice"] if pct >= 60 else COLORS["cyan"]
    return (
        '<div class="conf-row">'
        f'<div class="conf-track"><div class="conf-fill" style="width:{pct:.0f}%;'
        f'background:{color};"></div></div>'
        f'<span class="conf-num" style="color:{color}">{pct:.1f}%</span>'
        "</div>"
    )
