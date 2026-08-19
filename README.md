# DSV Ceph AI — decision dashboard

Visual front end for **Octopus Ceph** (DSV FlowAgent): the agent ingests logistics data in any
format, scores every suggested decision, and routes it to a machine or a human. This dashboard is
the operations view of that pipeline.

```
Layer 1  ingestion        CSV · JSON · PDF · TXT from partners, customers and DSV TMS instances
Layer 2  confidence       ML classifier scores each suggested decision 0–100%
Layer 3  decision router  ≥ threshold executes automatically, below it queues for a human
```

Human verdicts are posted back to the agent as training signal.

## Run it

```bash
pip install -r requirements.txt
streamlit run app.py
```

Opens on <http://localhost:8501>. It runs on demo fixtures out of the box — no endpoint, no
credentials, nothing to configure. The header shows a **DEMO DATA** badge whenever that's the case.

## Connecting the live agent

One environment variable. No UI changes.

```bash
# macOS / Linux
export CEPH_API_URL=https://your-agent-endpoint

# Windows PowerShell
$env:CEPH_API_URL = "https://your-agent-endpoint"
```

On Streamlit Cloud, put it in **Settings → Secrets** instead:

```toml
CEPH_API_URL = "https://your-agent-endpoint"
```

The badge flips to **LIVE AGENT** only once the endpoint actually answers. If it's configured but
unreachable or slow, the dashboard silently falls back to fixtures and keeps rendering — it will
never break mid-pitch.

### Endpoint contract

`agent_client.py` expects these routes. Full schemas are documented in that file's docstring.

| Method | Path | Returns |
|---|---|---|
| GET | `/shipments` | `{"shipments": [id, …]}` |
| GET | `/shipments/{id}` | shipment record (status, ETA, deadline, cargo, …) |
| GET | `/shipments/{id}/routes` | `{"routes": [{route, co2e_kg, transit_hours, hours_before_deadline, cost_eur, modes, baseline}]}` |
| GET | `/shipments/{id}/decisions` | `{"decisions": [{id, title, confidence, classification, action, rationale[]}]}` |
| GET | `/ingestion` | `{"feed": [{format, name, source, status, records}]}` |
| POST | `/chat` | `{"answer": "markdown"}` — body `{question, shipment_id}` |
| POST | `/feedback` | any 200 — body `{decision_id, verdict, shipment_id}` |

Only `/chat` is strictly required to make the assistant panel live; the rest can be adopted one at
a time, since each accessor falls back independently.

## Deploying

Push to GitHub, then on [share.streamlit.io](https://share.streamlit.io) point a new app at this
repo with `app.py` as the entrypoint. Add `CEPH_API_URL` to Secrets when the agent is ready.

### Access control

The app is open by default, which is what you want for a local demo or a screen-share. Set
`CEPH_PASSWORD` (env or Secrets) and it will ask for that code before rendering anything:

```toml
# .streamlit/secrets.toml  — gitignored
CEPH_PASSWORD = "pick-something"
```

Use it if the dashboard goes on a public Streamlit Cloud URL, because anyone with the link can
otherwise approve and reject decisions. It is a shared code, not an identity system — it cannot tell
you *who* approved something. Before this console drives real shipments, put proper SSO in front of
it (Streamlit's native `st.login()` OIDC, or an authenticating proxy).

## What's on screen

- **KPI strip** — shipment, customer, corridor, deadline buffer, CO2e against baseline, and how
  many decisions are waiting on a human.
- **Live status & delivery risk** — position, disruption cause, revised ETA against the contractual
  deadline, and the resulting on-track / at-risk / past-deadline band.
- **Decision queue** — every suggested action with its confidence meter, auto-approved or held for
  review against the threshold slider, and an expandable rationale. No black box.
- **Route comparison** — CO2e and remaining deadline buffer per route, with the baseline marked and
  the recommendation highlighted, plus the underlying numbers as a table.
- **Layer 1 ingestion feed** — what arrived, from whom, in what format, and whether it mapped.
- **Ask Ceph** — chat against the agent.

Move the **auto-decision threshold** slider to show routing shift live: at 60% everything executes
automatically, at 100% every decision lands on a human desk.

## Design

One palette, five blues — `#061a40` `#003559` `#0353a4` `#006daa` `#b9d6f2`. Squared corners
everywhere, no motion, no shadows. Colour carries meaning rather than decoration: the pale ice tone
marks whatever needs your attention (the recommended route, a decision awaiting review), mid blue is
a normal candidate, and the darkest blue is the booked baseline. Routes that arrive after the
deadline are drawn hollow with an ice outline — disqualified, not just worse.

## Files

| File | Role |
|---|---|
| `app.py` | Layout and all rendering |
| `theme.py` | Palette, CSS, Plotly treatment, HTML helpers |
| `auth.py` | Optional shared-password gate — inert unless `CEPH_PASSWORD` is set |
| `agent_client.py` | **The only integration point.** Live HTTP or fixtures |
| `static_data.py` | Demo fixtures — never imported outside `agent_client` |

That last rule is what makes the switch to live data a one-line change.
