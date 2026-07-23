---
description: Scan an MSP estate for automatable work and rank the candidates
argument-hint: "[only-automatable]"
---

You are helping an MSP decide what to automate, using the **Orchard** MCP server
(tools are namespaced `mcp__orchard__*`). Orchard has been watching this estate —
the technicians' activity stream and the ConnectWise ticket/time corpus — and can
surface the recurring, manual work that shouldn't be manual.

Do this:

1. **Run discovery.** Call `mcp__orchard__find_automatable_work`. It scans both
   sources (ambient activity + PSA tickets), upserts the candidates, and returns
   them ranked by time saved. (If the user only wants to re-read the current list
   without a fresh scan, call `mcp__orchard__list_discoveries` instead — pass
   `only_automatable: true` when `$ARGUMENTS` contains `only-automatable`.)

2. **Present the candidates as a prescriptive table**, richest first. For each:
   - **Title** and one-line pitch.
   - **Source** — `activity` (seen on a tech's screen) or `psa` (a recurring
     ConnectWise ticket category, priced from *logged* labor).
   - **Automatable** — `yes` / `partial` / `no`.
   - **Impact** — `est_minutes_week` and `est_dollars_week`, plus the evidence
     (`occurrences`, `distinct_days`, `distinct_users`).
   - **Suggested automation** — the `suggested_verbs` (the connector steps Orchard
     would wire, e.g. `action.connectwise:create_ticket`, `action.desktop_replay`).

3. **Recommend the top 1–3** to automate first, and say *why* (highest measured
   time, cleanest connector coverage, most techs affected). Be honest about the
   `partial` / `no` ones — don't oversell context-switching noise as automation.

4. **Explain how to accept.** Accepting a candidate turns it into a real,
   dynamic Orchard workflow (fields fill themselves at run time via trigger
   inputs + AI-filled fields — no hands on the keyboard). That step is an operator
   action in the Orchard console (**Discoveries → Accept**), which requires
   owner/admin sign-in — it is intentionally *not* an agent-executable MCP tool,
   because it creates an automation that can act on real systems.

Keep it concrete and short. This is a "what should we automate here, and what's it
worth?" answer, grounded in what Orchard actually measured — not generic advice.
