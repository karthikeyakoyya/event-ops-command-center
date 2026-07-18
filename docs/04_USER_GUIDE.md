# User Guide & Quick Start

## For the Field Marketing Team: How to Use This Day-to-Day

### 1. Researching a new event

1. Add a new row to the **Events** table in Airtable with the event name and URL. Leave Fit Score blank.
2. Run: `python event_research.py --event-name "Event Name Here"` (or paste in event page text if the event isn't easily searchable).
3. Refresh Airtable — the Fit Score, rationale, estimated audience size, and cost will be filled in.
4. Review the rationale. You make the final call on whether to move it to "Confirmed" — the score is a first-pass filter, not a decision-maker.

### 2. Tracking vendors

1. Add each vendor to the **Vendors** table, linked to its Event, with contract and payment deadlines filled in.
2. That's it — `vendor_watcher.py` runs automatically every morning and will flag anything at risk in Airtable (turns the Risk Flag red) and ping Slack if configured.
3. Check the dashboard's "Vendor Risk" panel each morning as part of your daily standup routine.

### 3. Generating outreach sequences

1. Once an event is Confirmed, add a Contact record (or a batch of them) with the target persona (e.g. "VP Finance," "RevOps Manager").
2. Run: `python outreach_sequencer.py --event-id "recXXXX" --persona "VP Finance"`.
3. Four draft emails (teaser, invite, reminder, follow-up) appear in the **Contacts/Outreach** table with Status = "Draft."
4. Edit as needed, then flip Status to "Approved" before sending through your actual email tool (Outreach, HubSpot, Gmail — this system generates drafts, it doesn't send).

### 4. Post-event reporting

1. After the event, fill in actuals in the **Events** table (final cost) and add lead count / notes.
2. Run: `python report_generator.py --event-id "recXXXX"`.
3. A formatted Markdown report is generated in `reports/` and a summary is written back to the **Reports** table — ready to paste into a deck or share directly with leadership.

### 5. The Dashboard

Visit your deployed Vercel URL for an at-a-glance view of:
- Upcoming events and their fit scores
- Vendor risk (red/yellow/green)
- Outreach sequences pending approval
- Historical event ROI trends

The dashboard is **read-only by design** — all edits happen in Airtable, keeping one clear source of truth.

## Quick Reference Card

| I want to... | Do this |
|---|---|
| Add a new event to evaluate | New row in Events table → run `event_research.py` |
| Check what's at risk this week | Open dashboard "Vendor Risk" panel |
| Draft outreach for an event | Run `outreach_sequencer.py --event-id ... --persona ...` |
| Get a post-event ROI summary | Fill in actuals → run `report_generator.py` |
| See historical performance | Dashboard → "ROI Trends" |
