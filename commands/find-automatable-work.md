---
description: Scan an MSP estate for automatable work and rank the candidates
argument-hint: "[only-automatable]"
---

You are helping an MSP decide what to automate, using the **Orchard** MCP server.
Tool names below are the server's own; your client namespaces them per server, so
they may surface as `mcp__…orchard__<tool>`. Orchard has been watching this estate —
the technicians' activity stream and the PSA's tickets and time (ConnectWise,
Autotask, HaloPSA or Kaseya BMS) — and can surface the recurring, manual work that
shouldn't be manual.

Do this:

1. **Run discovery.** Call `find_automatable_work`. It scans both
   sources (ambient activity + PSA tickets), upserts the candidates, and returns
   them ranked by time saved. (If the user only wants to re-read the current list
   without a fresh scan, call `list_discoveries` instead — pass
   `only_automatable: true` when `$ARGUMENTS` contains `only-automatable`.)

2. **Present the candidates as a prescriptive table**, richest first. For each:
   - **Title** and one-line pitch.
   - **Source** — `activity` (seen on a tech's screen) or `psa` (a recurring PSA
     ticket category, priced from *logged* time; where none was logged it falls back
     to a default handle time, and its pitch says "estimated").
   - **Automatable** — `yes` / `partial` / `no`.
   - **Impact** — `est_minutes_week` and `est_dollars_week`, plus the evidence
     (`occurrences`, `distinct_days`, `distinct_users`).
   - **Suggested automation** — the `suggested_verbs` (the connector steps Orchard
     would wire, e.g. `action.connectwise:create_ticket`, `action.desktop_replay`).

3. **Recommend the top 1–3** to automate first, and say *why* (highest measured
   time, cleanest connector coverage, most techs affected). Be honest about the
   `partial` / `no` ones — don't oversell context-switching noise as automation.

4. **Explain how to accept.** Accepting a candidate turns it into a **draft**
   playbook, never a live one. In Orchard that is **Build it** on the candidate under
   **Insights → Recommendations** (owner/admin). From here, `/automate` does it:
   `build_workflow` with `from_discovery_id` saves the draft, links the candidate and
   marks it accepted. Either way the draft runs nothing until a person reviews it and
   turns it on in Orchard.

Keep it concrete and short. This is a "what should we automate here, and what's it
worth?" answer, grounded in what Orchard actually measured — not generic advice.
