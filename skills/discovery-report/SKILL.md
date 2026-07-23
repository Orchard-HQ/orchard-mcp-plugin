---
name: discovery-report
description: Render Orchard automation-discovery results as a branded, deck-ready HTML report artifact. Use after calling the Orchard MCP find_automatable_work / list_discoveries tools when the user wants a shareable report (not just a table) of an MSP estate's automatable work.
---

# Orchard Discovery Report

Turn the discovery candidates the Orchard MCP tools return into a polished HTML
field report that matches Orchard's design — the same format as the Beacon /
Diamond / Titan reports.

## Input

An array of discovery candidates (from `find_automatable_work` or
`list_discoveries`). Each candidate carries:

- `title`, `pitch` — the named business process and one-line case.
- `source` — `"psa"` (a recurring ConnectWise ticket category, priced from logged
  labor) or `"activity"` (a repeated desktop ritual from the activity stream).
- `automatable` — `"yes" | "partial" | "no"`.
- `suggested_verbs` — the connector steps it maps to (e.g. `action.connectwise:create_ticket`).
- `est_minutes_week`, `est_dollars_week` — impact. `occurrences`, `distinct_days`,
  `distinct_users`, `distinct_machines` — evidence. `apps` — tools touched.
- `pattern` (if present) — the ordered `{app,title}` ritual; use it for the tool `.flow`.

## Steps

1. **Split by source.** `psa` candidates → the ranked ticket table. `activity`
   candidates → the ritual cards. Drop any `automatable == "no"`.
2. **Rank** each group by `est_minutes_week` descending.
3. **Compute the four hero stats** from the real data — e.g. total est. hours/week
   (sum of `est_minutes_week`/60), count rated `yes`, total candidates, and one
   estate-specific number (biggest single category, or techs affected). Never invent.
4. **Pick the accent** to match the estate's honest story and set `--accent` +
   `--accent-soft` in the template's `:root`:
   - `ember` (#ff7a45 / rgba(255,122,69,0.14)) — a real goldmine.
   - `gold` (#e6b23c / rgba(230,178,60,0.14)) — value buried under mess / a caveat.
   - `ice` (#86b7c9 / rgba(134,183,201,0.13)) — thin, little to automate.
5. **Fill the template** at `${CLAUDE_PLUGIN_ROOT}/skills/discovery-report/template.html`
   — replace every `<!-- SLOT:* -->` region, leave the `<style>` block untouched.
   Write the result to `discovery-report-<estate>.html`.
6. **Publish it as an artifact** (favicon `🌳`, title `"<Estate> — Automation
   Discovery"`) if the Artifact tool is available; otherwise save the HTML file and
   give the user its path. Then print a 3-bullet summary of the top automatable work.

## Voice — stay honest

The engine's credibility is that it doesn't only ever find gold. If an estate is
thin (few `yes`, low hours), say so plainly in the lede and use the `ice` accent —
an accurate "not much here" is a feature, not a failure. Dollar figures are
rate-dependent: label the assumed rate; hours are measured, so state them flatly.
