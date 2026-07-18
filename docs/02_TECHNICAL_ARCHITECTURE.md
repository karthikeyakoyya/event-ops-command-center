# Technical Architecture

## Stack Choice & Justification

| Layer | Choice | Why |
|---|---|---|
| System of record | **Airtable** | Best balance of spreadsheet familiarity + real relational structure + a mature REST API. Notion's API is weaker for structured automation (no real formula/rollup access, clunkier filtering); ClickUp is heavier than needed. Airtable lets non-technical teammates edit data directly while automation scripts read/write the same tables. |
| AI layer | **Claude API** (`claude-sonnet-4-6`) | Used for research synthesis, email generation, and report writing — tasks requiring judgment and natural language, not just data transformation. |
| Automation runner | **Python scripts**, scheduled via **GitHub Actions** (cron) | No paid infrastructure required; free, auditable, version-controlled. |
| Frontend | **React + Vite**, deployed on **Vercel** | Fast to build, free hosting tier, connects directly to Airtable's REST API client-side (read-only views) with automation results already written back to Airtable. |
| Optional integrations | **Zapier** (webhook bridge to Slack for alerts) | Adds real value (instant Slack pings on vendor risk) without custom infra. |

## System Diagram (data flow)

```
                     ┌─────────────────────┐
                     │   Airtable Base      │
                     │  (system of record)  │
                     │                      │
                     │  Events | Vendors    │
                     │  Contacts | Reports  │
                     └───────┬──────┬───────┘
                             │      │
              reads/writes   │      │  reads (views)
                             ▼      ▼
      ┌──────────────────────────┐   ┌───────────────────┐
      │   Automation Scripts     │   │  React Dashboard   │
      │   (Python, GH Actions)   │   │  (Vercel, read-only│
      │                          │   │  + trigger buttons)│
      │  1. event_research.py    │   └───────────────────┘
      │  2. vendor_watcher.py    │
      │  3. outreach_sequencer.py│
      │  4. report_generator.py  │
      └───────────┬──────────────┘
                  │
                  ▼
         ┌─────────────────┐        ┌───────────────┐
         │  Claude API      │───────▶│ Zapier webhook│──▶ Slack alert
         │ (reasoning layer)│        └───────────────┘
         └─────────────────┘
```

## Automation Triggers

| Script | Trigger | What it does |
|---|---|---|
| `event_research.py` | Manual run, or new row added to "Candidate Events" table | Takes a raw event name/URL, uses Claude with web-search-style prompting (or manually pasted event page text) to extract audience size, cost, dates, competitor sponsors, and outputs a 1–5 fit score with rationale. Writes back to Airtable. |
| `vendor_watcher.py` | Daily via GitHub Actions cron | Scans "Vendors" table for contracts unsigned within 5 days of deadline, or payments unconfirmed 3 days past due. Sends Slack alert via Zapier webhook and flags the record red in Airtable. |
| `outreach_sequencer.py` | Manual run, triggered from dashboard button or new "Campaign" record | Given event context + audience persona, generates a 4-touch email sequence (pre-event teaser, invite, reminder, post-event follow-up) via Claude, writes drafts into "Outreach" table for human review. |
| `report_generator.py` | Manual run, post-event | Pulls leads/costs/notes from Airtable for a given event, has Claude synthesize an executive ROI summary (structured JSON), and generates a formatted Markdown/PDF report. |

## Data Model (Airtable Base: "Event Ops")

**Table: Events**
- Event Name, URL, Dates, Location, Cost, Audience Size, Competitor Presence, Fit Score (1-5), Fit Rationale, Status (Researching / Confirmed / Live / Completed)

**Table: Vendors**
- Vendor Name, Linked Event, Contract Status, Contract Deadline, Payment Status, Payment Due Date, Contact Email, Risk Flag (auto-set)

**Table: Contacts / Outreach**
- Contact Name, Company, Persona, Linked Event, Sequence Stage, Draft Email Body, Status (Draft / Approved / Sent)

**Table: Post-Event Reports**
- Linked Event, Leads Captured, Total Cost, Cost per Lead, Notable Wins, Notable Issues, AI-Generated Summary, Report File Link

## Why This Design Works

- **Airtable as single source of truth** means humans and scripts never fight over where data lives — scripts read/write the same tables a coordinator edits by hand.
- **Claude is scoped to well-defined, structured tasks** (score this event, draft this sequence, summarize this data) rather than open-ended agentic behavior — this keeps outputs reliable and reviewable, and keeps API costs predictable.
- **No infrastructure to maintain**: GitHub Actions + Vercel + Airtable are all free-tier-friendly and require no servers to patch or pay for.
- **Human-in-the-loop by design**: every AI output (fit scores, email drafts, report summaries) lands as a *draft* in Airtable for review, never auto-sent or auto-published. This matters for both trust and inspecting the pattern-level correctness.
