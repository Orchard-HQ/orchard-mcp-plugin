---
description: A grounded brief on this MSP estate — what's there, where the time goes, what needs attention
argument-hint: "[optional: client name to scope to]"
---

Brief the user on this MSP estate using the Orchard MCP server. Tool names below are
the server's own; your client namespaces them per server, so they may surface as
`mcp__…orchard__<tool>`. Ground every claim in a tool result — no generic MSP advice.

1. **Orient.** `estate_overview`. This gives you the shape of everything: fleet and
   client counts, workflows by status, open signals, which PSA is wired (ConnectWise,
   Autotask, HaloPSA or Kaseya BMS, under `connectors`), **freshness per source**, and
   the governance posture. Read the freshness before anything else — a number from a
   source that last reported three weeks ago gets labelled as such, every time.
2. **Gather**, scoping to `$ARGUMENTS` where a tool takes `client_id`:
   - `activity_summary` — where the fleet's hours actually go, plus shadow AI.
   - `list_signals` with `state: "open"` — what's currently asking for a human.
   - `workflow_estate` — the automation's pulse and drift.
   - `savings_ledger` — the capacity estimates for what activated automation has
     returned, from completed runs against the manual baseline frozen when each went
     live. They are estimates, not measured time or cash saved; read its method.
   - `list_discoveries` — the automatable work already surfaced.
   Skip any tool whose source `estate_overview` shows as never-reported, and say you
   skipped it.
3. **Write the brief**, in this order and no longer than it needs to be:
   - **What this estate is** — one paragraph. Size, clients, connectors, posture.
   - **Where the time goes** — the top few sinks with real hours.
   - **What's asking for attention** — open signals by severity, failing playbooks,
     anything drifting.
   - **What's working** — live playbooks and the ledger's capacity estimates,
     labelled as estimates. If the ledger is empty because nothing has been
     activated, or a playbook has no frozen baseline, say exactly that: a gap, not
     zero.
   - **The one thing to do next**, and why it's that one.
4. **Caveats last, not buried.** Stale sources, unmapped techs (`list_team` reports
   them), a PSA that isn't wired — anything that makes a number above less
   trustworthy than it looks.
