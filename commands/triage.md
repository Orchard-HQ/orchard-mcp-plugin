---
description: Triage what needs a human right now — open signals, failed runs, pending self-heals
argument-hint: "[optional: severity, e.g. critical]"
---

Triage this MSP estate's open work using the Orchard MCP server. Tool names below are
the server's own; your client namespaces them per server, so they may surface as
`mcp__…orchard__<tool>`. The job is to turn a pile of facts into a short, ordered
list of what a person should do next.

1. **Signals.** `list_signals` with `state: "open"` (pass `severity` if
   `$ARGUMENTS` names one). Each signal carries its `source` and a `confidence` —
   a parsed inference and a heartbeat are not the same evidence, so don't rank them
   the same. `owner: null` means **nobody has this yet**; call that out explicitly,
   it's the most actionable thing on the page.
2. **Failed runs.** `list_runs`, then `get_run` on the failures for the per-step
   trail. Name the step that failed and what it reported — not "the workflow failed".
3. **Pending self-heals.** `list_heals` with `status: "pending"`. Each is a broken
   desktop selector with a proposed replacement awaiting a human. Note which
   playbooks appear more than once: a playbook that keeps healing is mis-compiled,
   and repairing it beats approving another patch.
4. **SLA pressure**, if ConnectWise is wired: `list_tickets` with
   `breached_sla: true, open_only: true`.

Then produce:

- **Do now** — up to 5 items, most consequential first. For each: what it is, the
  evidence (which tool said so), and the specific next action.
- **Watching** — real but not urgent, one line each.
- **Noise** — anything you'd suggest dismissing, and why.

Two rules. **Attribute every item to the tool result it came from.** And **do not
act** — approving a heal, resolving a signal and arming a playbook are all operator
actions in the Orchard console. The one thing you can do is pull the brake:
`set_workflow_status` can disable a playbook that's actively causing damage. Say so
if you think that's warranted, and let the user decide.
