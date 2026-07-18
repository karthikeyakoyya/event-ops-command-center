# Event Ops Command Center

**Live dashboard:** https://event-ops-command-center-buuz.vercel.app
**Source code:** https://github.com/karthikeyakoyya/event-ops-command-center

An AI-augmented system for field marketing event operations: research, vendor coordination, outreach sequencing, and post-event reporting — built on Airtable + Claude API + a custom dashboard.

## Start Here

1. Read `docs/01_PROJECT_VISION.md` — what this is and why it matters
2. Read `docs/02_TECHNICAL_ARCHITECTURE.md` — how it's built
3. Follow `docs/03_DEPLOYMENT_GUIDE.md` — step-by-step setup, 4-6 hours
4. Read `docs/04_USER_GUIDE.md` — how the team uses it day-to-day

## Folder Structure

```
event-ops-command-center/
├── README.md                        ← you are here
├── docs/
│   ├── 01_PROJECT_VISION.md
│   ├── 02_TECHNICAL_ARCHITECTURE.md
│   ├── 03_DEPLOYMENT_GUIDE.md
│   └── 04_USER_GUIDE.md
├── automation/                      ← Python scripts, run locally or via GitHub Actions
│   ├── airtable_client.py
│   ├── claude_client.py
│   ├── event_research.py
│   ├── vendor_watcher.py
│   ├── outreach_sequencer.py
│   ├── report_generator.py
│   ├── requirements.txt
│   └── .env.example
├── dashboard/                       ← React + Vite frontend, deploy to Vercel
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   └── src/
│       ├── main.jsx
│       ├── App.jsx
│       └── index.css
├── templates/                       ← ready-to-use templates
│   ├── vendor_checklist.md
│   ├── email_sequence_example.md
│   └── post_event_report_template.md
├── data/                            ← sample data for initial Airtable import
│   ├── sample_events.csv
│   ├── sample_vendors.csv
│   └── sample_contacts.csv
├── config/
│   └── airtable_schema.md           ← exact Airtable table/field setup
└── .github/workflows/
    └── vendor_watcher.yml           ← daily automated vendor risk check
```

## The Four Automated Workflows

1. **Event research** (`event_research.py`) — Claude scores candidate events for ICP fit
2. **Vendor coordination** (`vendor_watcher.py`) — daily automated risk flagging + Slack alerts
3. **Outreach sequencing** (`outreach_sequencer.py`) — Claude drafts 4-touch email sequences
4. **Post-event reporting** (`report_generator.py`) — Claude synthesizes ROI summaries

## License / Use

Built as a portfolio/demo project. Adapt freely for real team use — just make sure the API keys in `.env` are your own and never committed to version control.

