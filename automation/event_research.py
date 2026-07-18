"""
event_research.py

Given an event name (and optionally pasted event-page text), uses Claude to
extract structured details and produce a 1-5 fit score with rationale,
then writes the result back to the Airtable "Events" table.

Usage:
    python event_research.py --event-name "SaaStr Annual 2026" --test
    python event_research.py --record-id "recXXXXXXXX" --context-file event_page.txt
"""

import argparse
from claude_client import ask_claude_for_json
from airtable_client import list_records, update_record, TABLE_EVENTS

SYSTEM_PROMPT = """You are a senior field marketing strategist evaluating B2B SaaS
conferences and events for sponsorship/attendance fit. The company is Zenskar,
a usage-based billing and revenue automation platform selling primarily to
finance and RevOps leaders (VP Finance, Controller, Head of RevOps, CFO) at
mid-market and enterprise SaaS companies.

Given information about a candidate event, evaluate:
- Audience fit (does the attendee base include finance/RevOps/billing personas?)
- Estimated cost tier (sponsorship + travel, rough order of magnitude)
- Competitor presence (are direct competitors in usage-based billing / CPQ /
  subscription management likely to sponsor or attend?)
- Overall fit score from 1 (poor fit) to 5 (excellent fit)

Be honest and calibrated. A 5 should be rare and well-justified. If you don't
have reliable information about an event, say so in the rationale rather than
fabricating specifics."""


def build_user_prompt(event_name, context_text=None):
    prompt = f"Event to evaluate: {event_name}\n\n"
    if context_text:
        prompt += f"Additional context (pasted from event page):\n{context_text}\n\n"
    prompt += """Respond with a JSON object with exactly these keys:
{
  "estimated_audience_size": "string, e.g. '2000-3000 attendees' or 'unknown'",
  "estimated_cost_tier": "string, e.g. '$15k-25k sponsorship' or 'unknown'",
  "competitor_presence": "string describing likely competitor presence",
  "fit_score": integer from 1 to 5,
  "fit_rationale": "2-3 sentence explanation of the score, noting any uncertainty"
}"""
    return prompt


def research_event(event_name, context_text=None):
    user_prompt = build_user_prompt(event_name, context_text)
    return ask_claude_for_json(SYSTEM_PROMPT, user_prompt)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--event-name", help="Name of the event to research")
    parser.add_argument("--record-id", help="Airtable record ID to update directly")
    parser.add_argument("--context-file", help="Path to a text file with pasted event page content")
    parser.add_argument("--test", action="store_true", help="Print results without writing to Airtable")
    args = parser.parse_args()

    if not args.event_name and not args.record_id:
        parser.error("Provide --event-name or --record-id")

    context_text = None
    if args.context_file:
        with open(args.context_file, "r") as f:
            context_text = f.read()

    event_name = args.event_name
    record_id = args.record_id

    if record_id and not event_name:
        record = None
        for r in list_records(TABLE_EVENTS):
            if r["id"] == record_id:
                record = r
                break
        if not record:
            raise ValueError(f"No record found with id {record_id}")
        event_name = record["fields"].get("Event Name", "")

    print(f"Researching: {event_name}")
    result = research_event(event_name, context_text)

    print("\n--- Claude's Assessment ---")
    for k, v in result.items():
        print(f"{k}: {v}")

    fields = {
        "Fit Score": result["fit_score"],
        "Fit Rationale": result["fit_rationale"],
        "Audience Size": result["estimated_audience_size"],
        "Cost": result["estimated_cost_tier"],
        "Competitor Presence": result["competitor_presence"],
    }

    if args.test:
        print("\n[TEST MODE] Not writing to Airtable. Fields that would be written:")
        print(fields)
        return

    if not record_id:
        print(
            "\nNo --record-id provided; results printed above only. "
            "Pass --record-id to write these back to an existing Airtable row."
        )
        return

    update_record(TABLE_EVENTS, record_id, fields)
    print(f"\nUpdated Airtable record {record_id}.")


if __name__ == "__main__":
    main()
