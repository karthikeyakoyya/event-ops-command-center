# Step-by-Step Deployment Guide

Estimated total setup time: **4–6 hours** spread over 2–3 days (most of it is Airtable schema setup and API key provisioning; the code itself is ready to run).

## Phase 0: Prerequisites

- [ ] An Airtable account (free tier is sufficient to start)
- [ ] An Anthropic API key (console.anthropic.com → get API key)
- [ ] A GitHub account (for hosting code + running scheduled automations via Actions)
- [ ] A Vercel account (free tier, for the dashboard)
- [ ] (Optional) A Zapier account free tier, and a Slack workspace, for alerting
- [ ] Python 3.10+ installed locally, Node 18+ installed locally

## Phase 1: Airtable Base Setup (45–60 min)

1. Create a new Airtable Base named **"Event Ops"**.
2. Create four tables exactly as specified in `docs/02_TECHNICAL_ARCHITECTURE.md` → Data Model section: `Events`, `Vendors`, `Contacts`, `Reports`.
3. For each table, add the fields listed, using these Airtable field types:
   - Text fields → Single line text / Long text (for rationale, email bodies)
   - Dates → Date field
   - Status/Risk Flag → Single select (with color coding: green/yellow/red)
   - Cost/Audience Size → Number/Currency
   - Linked Event → Link to another record (relational join to `Events`)
4. Go to **Account → Developer Hub → Personal Access Tokens**, create a token with `data.records:read` and `data.records:write` scopes for this base. Copy the token — you'll need it as `AIRTABLE_API_KEY`.
5. Note your **Base ID** (found in the API docs section of the base, or in the base URL: `airtable.com/appXXXXXXXXXXXXXX/...` — the `appXXXX` part is your Base ID).

## Phase 2: Local Project Setup (20 min)

```bash
git clone <your-repo-url> event-ops-command-center
cd event-ops-command-center

# Python automation environment
cd automation
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt --break-system-packages

# Frontend
cd ../dashboard
npm install
```

## Phase 3: Configure Environment Variables (10 min)

Copy the example env file and fill in your keys:

```bash
cd automation
cp .env.example .env
```

Edit `.env`:
```
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxx
AIRTABLE_API_KEY=patXXXXXXXXXXXXXX
AIRTABLE_BASE_ID=appXXXXXXXXXXXXXX
SLACK_WEBHOOK_URL=https://hooks.zapier.com/hooks/catch/xxxx/xxxx/   # optional
```

**Never commit `.env` to git** — it's already listed in `.gitignore`.

## Phase 4: Test Each Automation Script Locally (30–45 min)

Run each script against a test record before scheduling anything:

```bash
python event_research.py --event-name "SaaStr Annual 2026" --test
python vendor_watcher.py --dry-run
python outreach_sequencer.py --event-id "recXXXXXXXX" --persona "VP Finance"
python report_generator.py --event-id "recXXXXXXXX"
```

Each script prints what it *would* write to Airtable when run with `--dry-run` or `--test`, so you can sanity-check output before it touches real data.

## Phase 5: Schedule Automations via GitHub Actions (20 min)

1. Push the repo to GitHub.
2. In the repo, go to **Settings → Secrets and variables → Actions** and add each `.env` value as a repository secret (`ANTHROPIC_API_KEY`, `AIRTABLE_API_KEY`, `AIRTABLE_BASE_ID`, `SLACK_WEBHOOK_URL`).
3. The workflow file at `.github/workflows/vendor_watcher.yml` is already configured to run `vendor_watcher.py` daily at 8am. Confirm it's enabled under the repo's **Actions** tab.
4. `event_research.py`, `outreach_sequencer.py`, and `report_generator.py` are designed for on-demand runs (triggered from the dashboard or manually) rather than schedules, since they need a specific event as input.

## Phase 6: Deploy the Dashboard (20–30 min)

```bash
cd dashboard
npm run build
```

1. Push the `dashboard/` folder to GitHub (same repo or separate).
2. In Vercel: **New Project → Import Git Repository** → select the repo → set root directory to `dashboard/`.
3. Add environment variables in Vercel's project settings: `VITE_AIRTABLE_API_KEY`, `VITE_AIRTABLE_BASE_ID` (read-only scoped token recommended for the frontend).
4. Deploy. Vercel will give you a live URL (e.g., `event-ops-command-center.vercel.app`).

## Phase 7: (Optional) Slack Alerts via Zapier (15 min)

1. Create a Zap: **Trigger** = "Catch Hook" (Webhooks by Zapier).
2. Copy the generated webhook URL into `.env` as `SLACK_WEBHOOK_URL`.
3. **Action** = Slack → "Send Channel Message", mapping the webhook's `message` field into the Slack message body.
4. Turn the Zap on.

## Go-Live Testing Checklist

- [ ] Airtable base has all 4 tables with correct field types and at least 2–3 rows of sample/seed data (see `data/` folder)
- [ ] All 4 Python scripts run successfully in `--dry-run`/`--test` mode with no errors
- [ ] `.env` secrets are correctly set both locally and in GitHub Actions secrets
- [ ] GitHub Actions workflow for `vendor_watcher.py` shows a successful run in the Actions tab
- [ ] Dashboard loads at the Vercel URL and correctly displays live Airtable data
- [ ] Slack alert test fires correctly when a vendor record is manually set to a "past deadline" state
- [ ] At least one full dry run of each of the 4 workflows has been reviewed by a human before going live with real event data

## Post-Deployment Monitoring & Maintenance

- **Weekly**: Spot-check 2–3 AI-generated outputs (fit scores, email drafts, report summaries) against your own judgment to catch prompt drift or bad outputs early.
- **Monthly**: Review Anthropic API usage/cost in the Anthropic Console; these workloads are low-volume and should stay inexpensive (well under $10/month at typical event cadence).
- **On schema change**: If you add/rename Airtable fields, update the corresponding field-name constants at the top of each Python script — they're centralized specifically to make this a one-line change.
- **On GitHub Actions failure**: Check the Actions tab logs first; the most common cause is an expired Airtable personal access token (tokens can be set to auto-expire — set a calendar reminder to rotate it).
