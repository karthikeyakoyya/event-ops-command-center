import React, { useEffect, useState } from "react";

// ---------------------------------------------------------------------------
// DATA LAYER
// In production, replace the sample arrays below with live fetches to the
// Airtable REST API (VITE_AIRTABLE_API_KEY / VITE_AIRTABLE_BASE_ID — see
// docs/03_DEPLOYMENT_GUIDE.md, Phase 6). This dashboard is read-only by
// design: all edits happen in Airtable, automations write the AI-generated
// fields, and this view just displays them.
// ---------------------------------------------------------------------------

const events = [
  { name: "SaaStr Annual 2026", date: "Sep 8–10", city: "San Francisco, CA", fit: 5, status: "Researching" },
  { name: "RevOps Unplugged", date: "Nov 5–6", city: "Denver, CO", fit: 4, status: "Researching" },
  { name: "Finance Leaders Summit", date: "Oct 14–15", city: "Austin, TX", fit: 4, status: "Confirmed" },
  { name: "DevOps Days Local", date: "Aug 20", city: "Chicago, IL", fit: 2, status: "Researching" },
];

const vendors = [
  { name: "Swag & Co", event: "Finance Leaders Summit", risk: "brick", reason: "Contract unsigned, deadline in 2 days" },
  { name: "BoothWorks Displays", event: "SaaStr Annual 2026", risk: "brass", reason: "Contract deadline in 8 days" },
  { name: "Elite AV Rentals", event: "SaaStr Annual 2026", risk: "forest", reason: "Signed and paid" },
  { name: "Catering Partners LLC", event: "RevOps Unplugged", risk: "forest", reason: "Signed, payment on track" },
];

const outreach = [
  { contact: "Jordan Ellis", company: "Northwind SaaS", stage: "Teaser", status: "Draft" },
  { contact: "Priya Nair", company: "Cascade Analytics", stage: "Teaser", status: "Draft" },
  { contact: "Marcus Webb", company: "Fielding Software", stage: "Invite", status: "Approved" },
];

const roiTrend = [
  { event: "Q1 Summit", costPerLead: 42 },
  { event: "Cloud Connect", costPerLead: 31 },
  { event: "FinOps Live", costPerLead: 55 },
  { event: "RevOps Days", costPerLead: 28 },
];

const riskTokens = {
  brick: { fg: "var(--brick)", bg: "var(--brick-soft)", label: "At risk" },
  brass: { fg: "var(--brass)", bg: "var(--brass-soft)", label: "Watch" },
  forest: { fg: "var(--forest)", bg: "var(--forest-soft)", label: "On track" },
};

function useToday() {
  const [now] = useState(new Date());
  return now.toLocaleDateString(undefined, { weekday: "long", month: "long", day: "numeric" });
}

// Elegant thin-line trend chart, single hue, quiet dot markers.
function TrendLine({ data }) {
  const w = 460;
  const h = 130;
  const padX = 18;
  const padY = 18;
  const max = Math.max(...data.map((d) => d.costPerLead));
  const min = 0;
  const step = (w - padX * 2) / (data.length - 1);

  const points = data.map((d, i) => {
    const x = padX + i * step;
    const y = h - padY - ((d.costPerLead - min) / (max - min)) * (h - padY * 2);
    return { x, y, ...d };
  });

  const path = points.map((p, i) => `${i === 0 ? "M" : "L"} ${p.x} ${p.y}`).join(" ");

  return (
    <svg viewBox={`0 0 ${w} ${h}`} width="100%" height={h} style={{ overflow: "visible" }}>
      <line x1={padX} y1={h - padY} x2={w - padX} y2={h - padY} stroke="var(--hairline)" strokeWidth="1" />
      <path d={path} fill="none" stroke="var(--forest)" strokeWidth="1.75" />
      {points.map((p, i) => (
        <g key={i}>
          <circle cx={p.x} cy={p.y} r="3.5" fill="var(--card)" stroke="var(--forest)" strokeWidth="1.5" />
          <text x={p.x} y={p.y - 12} textAnchor="middle" fontSize="11" fontFamily="var(--font-mono)" fill="var(--ink-soft)">
            ${p.costPerLead}
          </text>
          <text x={p.x} y={h + 2} textAnchor="middle" fontSize="10" fontFamily="var(--font-mono)" fill="var(--muted)">
            {p.event}
          </text>
        </g>
      ))}
    </svg>
  );
}

function FitMarks({ score }) {
  return (
    <span style={{ display: "inline-flex", gap: 3 }}>
      {Array.from({ length: 5 }).map((_, i) => (
        <span
          key={i}
          style={{
            width: 5,
            height: 5,
            borderRadius: "50%",
            background: i < score ? "var(--brass)" : "var(--hairline)",
          }}
        />
      ))}
    </span>
  );
}

export default function App() {
  const today = useToday();
  const avgCostPerLead = Math.round(
    roiTrend.reduce((sum, r) => sum + r.costPerLead, 0) / roiTrend.length
  );
  const flaggedCount = vendors.filter((v) => v.risk !== "forest").length;

  return (
    <div className="app">
      <style>{styles}</style>

      <header className="top">
        <div>
          <div className="eyebrow">Zenskar &middot; Field Marketing</div>
          <h1 className="wordmark">Event Ops</h1>
        </div>
        <div className="top-date">{today}</div>
      </header>

      <section className="hero">
        <div className="hero-figure">
          <div className="hero-label">Trailing average cost per lead</div>
          <div className="hero-number">${avgCostPerLead}</div>
          <div className="hero-sub">across the last four events</div>
        </div>
        <div className="hero-chart">
          <TrendLine data={roiTrend} />
        </div>
      </section>

      <div className="layout">
        <main className="ledger">
          <div className="section-head">
            <h2>Upcoming events</h2>
            <span className="count">{events.length}</span>
          </div>

          <ol className="ledger-list">
            {events.map((e, i) => (
              <li key={e.name} className="ledger-row">
                <span className="ledger-index">{String(i + 1).padStart(2, "0")}</span>
                <div className="ledger-main">
                  <div className="ledger-name">{e.name}</div>
                  <div className="ledger-meta">
                    {e.date} &nbsp;&middot;&nbsp; {e.city}
                  </div>
                </div>
                <FitMarks score={e.fit} />
                <span className={`status-tag status-${e.status.toLowerCase()}`}>{e.status}</span>
              </li>
            ))}
          </ol>
        </main>

        <aside className="rail">
          <div className="section-head">
            <h2>Vendor risk</h2>
            <span className="count">{flaggedCount} flagged</span>
          </div>
          <ul className="rail-list">
            {vendors.map((v) => {
              const t = riskTokens[v.risk];
              return (
                <li key={v.name} className="rail-row">
                  <div className="rail-row-top">
                    <span className="rail-name">{v.name}</span>
                    <span className="rail-badge" style={{ color: t.fg, background: t.bg }}>
                      {t.label}
                    </span>
                  </div>
                  <div className="rail-event">{v.event}</div>
                  <div className="rail-reason">{v.reason}</div>
                </li>
              );
            })}
          </ul>

          <div className="section-head rail-second">
            <h2>Outreach queue</h2>
            <span className="count">{outreach.filter((o) => o.status === "Draft").length} in review</span>
          </div>
          <ul className="rail-list">
            {outreach.map((o, i) => (
              <li key={i} className="rail-row outreach-row">
                <div>
                  <div className="rail-name">{o.contact}</div>
                  <div className="rail-event">{o.company}</div>
                </div>
                <div className="outreach-tags">
                  <span className="stage-chip">{o.stage}</span>
                  <span className={`status-chip ${o.status === "Draft" ? "chip-draft" : "chip-approved"}`}>
                    {o.status}
                  </span>
                </div>
              </li>
            ))}
          </ul>
        </aside>
      </div>

      <footer className="foot">Synced from Airtable &middot; scored and drafted by Claude</footer>
    </div>
  );
}

const styles = `
  .app { max-width: 1040px; margin: 0 auto; padding: 48px 28px 72px; }

  .top {
    display: flex; justify-content: space-between; align-items: flex-end;
    margin-bottom: 40px;
  }
  .eyebrow {
    font-size: 12px; letter-spacing: 0.06em; text-transform: uppercase;
    color: var(--brass); margin-bottom: 6px;
  }
  .wordmark {
    font-family: var(--font-display); font-style: italic; font-weight: 500;
    font-size: 32px; margin: 0; color: var(--ink);
  }
  .top-date { font-size: 13px; color: var(--muted); }

  .hero {
    display: grid; grid-template-columns: 220px 1fr; gap: 40px; align-items: center;
    padding: 28px 0 40px; border-bottom: 1px solid var(--hairline); margin-bottom: 40px;
  }
  .hero-label { font-size: 12px; color: var(--muted); text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 6px; }
  .hero-number {
    font-family: var(--font-display); font-style: italic; font-weight: 500;
    font-size: 56px; line-height: 1; color: var(--forest);
  }
  .hero-sub { font-size: 13px; color: var(--muted); margin-top: 6px; }
  .hero-chart { padding-top: 6px; }

  .layout { display: grid; grid-template-columns: 1.5fr 1fr; gap: 56px; }

  .section-head {
    display: flex; align-items: baseline; justify-content: space-between;
    margin-bottom: 18px;
  }
  .section-head h2 {
    font-family: var(--font-display); font-weight: 500; font-size: 19px; margin: 0; color: var(--ink);
  }
  .count { font-family: var(--font-mono); font-size: 11px; color: var(--muted); }

  .ledger-list { list-style: none; margin: 0; padding: 0; }
  .ledger-row {
    display: grid; grid-template-columns: 32px 1fr auto 96px;
    align-items: center; gap: 16px;
    padding: 16px 0; border-top: 1px solid var(--hairline);
  }
  .ledger-row:last-child { border-bottom: 1px solid var(--hairline); }
  .ledger-index { font-family: var(--font-mono); font-size: 12px; color: var(--muted); }
  .ledger-name { font-size: 16px; color: var(--ink); }
  .ledger-meta { font-family: var(--font-mono); font-size: 11px; color: var(--muted); margin-top: 3px; }

  .status-tag {
    font-family: var(--font-mono); font-size: 10px; text-transform: uppercase;
    letter-spacing: 0.03em; padding: 4px 9px; border: 1px solid var(--hairline);
    color: var(--ink-soft); text-align: center; white-space: nowrap;
  }
  .status-confirmed { color: var(--forest); border-color: var(--forest); }

  .rail-second { margin-top: 40px; }
  .rail-list { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 18px; }
  .rail-row { padding-bottom: 18px; border-bottom: 1px solid var(--hairline); }
  .rail-row:last-child { border-bottom: none; padding-bottom: 0; }
  .rail-row-top { display: flex; justify-content: space-between; align-items: center; gap: 8px; }
  .rail-name { font-size: 14px; color: var(--ink); }
  .rail-badge {
    font-family: var(--font-mono); font-size: 10px; text-transform: uppercase;
    padding: 3px 8px; letter-spacing: 0.02em; white-space: nowrap;
  }
  .rail-event { font-family: var(--font-mono); font-size: 11px; color: var(--brass); margin-top: 3px; }
  .rail-reason { font-size: 12px; color: var(--muted); margin-top: 4px; }

  .outreach-row { display: flex; justify-content: space-between; align-items: flex-start; }
  .outreach-tags { display: flex; gap: 6px; }
  .stage-chip {
    font-family: var(--font-mono); font-size: 10px; color: var(--ink-soft);
    border: 1px solid var(--hairline); padding: 3px 8px;
  }
  .status-chip { font-family: var(--font-mono); font-size: 10px; padding: 3px 8px; }
  .chip-draft { color: var(--brass); background: var(--brass-soft); }
  .chip-approved { color: var(--forest); background: var(--forest-soft); }

  .foot {
    margin-top: 64px; font-size: 11px; color: var(--muted);
    border-top: 1px solid var(--hairline); padding-top: 18px;
  }

  @media (max-width: 780px) {
    .layout { grid-template-columns: 1fr; }
    .hero { grid-template-columns: 1fr; }
    .ledger-row { grid-template-columns: 24px 1fr; row-gap: 8px; }
    .ledger-row > *:nth-child(3), .ledger-row > *:nth-child(4) { grid-column: 2; }
  }
`;
