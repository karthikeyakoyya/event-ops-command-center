# Event Operations Command Center
### Project Vision Document

## What This Is

The Event Operations Command Center (EOCC) is an AI-augmented system that automates the four most time-consuming parts of running field marketing events:

1. **Event Research** — turning a raw list of candidate conferences/events into a ranked, qualified shortlist with sponsorship costs, audience fit, and competitor presence, automatically.
2. **Vendor Coordination** — a live tracker that watches vendor contracts, deadlines, and payment status, and proactively flags anything at risk before it becomes a fire drill.
3. **Outreach Sequencing** — Claude-generated, personalized multi-touch email sequences for pre-event, at-event, and post-event outreach to prospects and partners, pulled directly from event context.
4. **Post-Event Reporting** — turns raw event data (leads scanned, costs, attendee notes) into an executive-ready ROI report in minutes instead of days.

Airtable is the system of record. Claude API is the reasoning layer that reads Airtable data, does the thinking a coordinator would otherwise do by hand, and writes results back. A lightweight custom web dashboard (React, deployed on Vercel) sits on top as the "command center" view — the visual, at-a-glance layer stakeholders actually look at.

## Why This Matters for the Field Marketing & Events Role

Field marketing at a B2B SaaS company like Zenskar runs on a brutal amount of manual coordination: researching which events are worth the spend, chasing vendors for signed contracts and booth specs, writing outreach emails to the same personas over and over with slightly different context, and building ROI decks after the event when everyone has already moved on to the next one.

None of that work is conceptually hard. It's just repetitive, detail-heavy, and easy to drop a ball on. That makes it exactly the kind of work AI-augmented tooling is good at — not replacing judgment, but doing the first draft of the thinking and the coordination legwork so a human only has to review, adjust, and decide.

## Business Impact (Quantified Estimates)

| Workflow | Manual Time (per event) | With EOCC | Time Saved |
|---|---|---|---|
| Event research & qualification | 3–4 hrs per 10 candidate events | ~30 min review | ~85% |
| Vendor status tracking & follow-ups | 2–3 hrs/week | ~20 min/week | ~85% |
| Outreach sequence drafting | 2 hrs per campaign | ~15 min review/edit | ~87% |
| Post-event ROI report | 4–6 hrs | ~45 min review | ~85% |

Across a quarter running 4–6 events, this conservatively saves **35–50 hours** of coordination work — time that converts directly into more events run per headcount, or the same events run with meaningfully less risk of dropped follow-ups.

Beyond time savings:
- **Fewer missed follow-ups**: automated flags on vendor deadlines and outreach cadence remove reliance on memory and manual calendar-checking.
- **Real-time pipeline visibility**: leadership can see event pipeline, vendor risk, and historical ROI in one dashboard instead of scattered spreadsheets and Slack threads.
- **Faster, more consistent outreach**: every sequence is grounded in the same context (event details, ICP, past performance) instead of being rewritten from scratch or copy-pasted with mismatched details.

## Why This Is a Strong Portfolio Piece

It's not a toy CRUD app. It demonstrates:
- Structured data modeling (Airtable schema design for a real operational workflow)
- Practical AI integration (prompt design, structured JSON outputs, using an LLM as a workflow engine rather than a chatbot)
- Full-stack delivery (API integration + automation scripts + a deployed frontend)
- Product thinking — the project is scoped around a real role's actual pain points, not a generic demo
