"""
report_generator.py

Pulls actuals for a completed event from Airtable, uses Claude to synthesize
an executive-ready ROI summary, and writes both a Markdown report file and
a summary record back to Airtable.

Usage:
    python report_generator.py --event-id "recXXXXXXXX"
"""

import argparse
import os
from datetime import datetime

from claude_client import ask_claude_for_json
from airtable_client import get_record, create_record, TABLE_EVENTS, TABLE_REPORTS

SYSTEM_PROMPT = """You are a field marketing analyst writing a concise,
executive-ready post-event ROI summary for internal leadership at Zenskar.
Be honest about both wins and shortfalls. Do not inflate results. Use plain
numbers and avoid marketing fluff."""


def build_user_prompt(event_fields):
    return f"""Event: {event_fields.get('Event Name')}
Total Cost: {event_fields.get('Cost', 'unknown')}
Leads Captured: {event_fields.get('Leads Captured', 'unknown')}
Notes from team: {event_fields.get('Notes', 'none provided')}

Respond with a JSON object with exactly these keys:
{{
  "cost_per_lead": "string, computed if cost and lead count are available, else 'unable to calculate'",
  "executive_summary": "3-4 sentence summary of overall event performance",
  "notable_wins": "1-2 sentence summary of what went well",
  "notable_issues": "1-2 sentence summary of what didn't go well or should change next time",
  "recommendation": "1 sentence: repeat this event next year, or not, and why"
}}"""


def generate_report(event_fields):
    user_prompt = build_user_prompt(event_fields)
    return ask_claude_for_json(SYSTEM_PROMPT, user_prompt)


def write_markdown_report(event_name, analysis, output_dir="../reports"):
    os.makedirs(output_dir, exist_ok=True)
    filename = f"{output_dir}/{event_name.replace(' ', '_')}_report_{datetime.today().strftime('%Y%m%d')}.md"
    content = f"""# Post-Event Report: {event_name}
Generated: {datetime.today().strftime('%Y-%m-%d')}

## Executive Summary
{analysis['executive_summary']}

## Cost per Lead
{analysis['cost_per_lead']}

## Notable Wins
{analysis['notable_wins']}

## Notable Issues
{analysis['notable_issues']}

## Recommendation
{analysis['recommendation']}
"""
    with open(filename, "w") as f:
        f.write(content)
    return filename


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--event-id", required=True)
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args()

    event_record = get_record(TABLE_EVENTS, args.event_id)
    event_fields = event_record["fields"]
    event_name = event_fields.get("Event Name", "Unknown Event")

    print(f"Generating post-event report for '{event_name}'...")
    analysis = generate_report(event_fields)

    for k, v in analysis.items():
        print(f"\n{k}: {v}")

    filepath = write_markdown_report(event_name, analysis)
    print(f"\nMarkdown report written to: {filepath}")

    report_fields = {
        "Linked Event": [args.event_id],
        "AI-Generated Summary": analysis["executive_summary"],
        "Cost per Lead": analysis["cost_per_lead"],
        "Notable Wins": analysis["notable_wins"],
        "Notable Issues": analysis["notable_issues"],
        "Report File Link": filepath,
    }

    if args.test:
        print("\n[TEST MODE] Would create Reports record with above fields.")
    else:
        create_record(TABLE_REPORTS, report_fields)
        print("Report record created in Airtable.")


if __name__ == "__main__":
    main()
