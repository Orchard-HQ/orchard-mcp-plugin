---
description: Audit every Orchard playbook for drift, fragility and dead weight
argument-hint: "[optional: playbook name to audit just one]"
---

Audit this MSP's automation estate using the Orchard MCP server. Tool names below are
the server's own; your client namespaces them per server, so they may surface as
`mcp__…orchard__<tool>`. The question is "is this automation still healthy", not "is
it valuable" — the ledger answers that one.

1. **Ground yourself first.** `estate_overview` — the governance posture and each
   source's freshness. A paused estate explains a roster of idle playbooks; a stale
   endpoint feed explains missing runs. Auditing without that context produces
   confident verdicts about the wrong thing.
2. **The roster.** `list_workflows`, then `workflow_estate` for each playbook's
   pulse and drift verdict plus the global brake state. If `$ARGUMENTS` names one,
   audit just that one, in more depth. Treat `unproven` as what it says — too few
   runs to rate, **not** a pass. A playbook that failed both its runs lands there.
3. **Per playbook**, gather and read:
   - `get_workflow` — the current graph and the linter's `warnings`.
   - `validate_workflow` with `workflow_id` — does what's *saved* still validate?
     A playbook that was valid when it was built can fail today if the catalog moved
     underneath it. Flag anything invalid as urgent: it will fail at run time.
   - `list_workflow_versions` — churn. Many versions in a short window means the
     shape was never right.
   - `get_workflow_evidence` — the Witness's receipts. `observed: 0` means the
     playbook was hand-built with no evidence behind it. That's allowed, but it's a
     different kind of confidence and should be labelled. `thin_evidence: true` means
     it was compiled from one or two recordings — quote `observed` alongside any
     confidence figure, never the figure alone.
   - `list_heals` for that `workflow_id` — repeated heals on the same node mean a
     fragile selector, not a resilient system.
   - `list_runs` / `get_run` — recent failure rate and which step fails.
4. **Report a table**, worst first: playbook, status, current version, valid?,
   run failure rate, heal count, evidence, verdict.
5. **Then the three lists:**
   - **Broken** — saved graphs that don't validate, or playbooks failing repeatedly.
     Say which step and why. Offer to fix each via `/workflow-edit`.
   - **Fragile** — healing repeatedly, drifting, or hand-built with no evidence.
   - **Dead weight** — active but never firing, or drafts that never got armed.
     Suggest `set_workflow_status` to archive, and let the user decide.

Don't rewrite anything in this command — audit, report, and offer. Edits go through
`/workflow-edit` so the diff gets reviewed before it's saved.
