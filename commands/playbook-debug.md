---
description: Diagnose a failing playbook step by step — reproduce the failure at the cheapest honest rung, fix the cause, prove the fix
argument-hint: "[playbook name or run id — omit to start from the newest failed run]"
---

Debug an Orchard playbook using the MCP diagnostics tools, following the
workflow-troubleshooting skill. Tool names below are the server's own; your
client namespaces them per server, so they may surface as
`mcp__…orchard__<tool>`.

1. **Find the failure.** If `$ARGUMENTS` names a run id, `get_run` it. If it
   names a playbook, `get_workflow` then `list_runs` for its newest failure.
   Bare: `list_runs` and take the newest failed run. The failing step's
   rendered `input` and its error are the whole starting point — quote both.
2. **Reproduce at the cheapest rung.** `test_workflow_node` for the failing
   node with `context_run_id` set to the failed run — same step, same data.
   For a ConnectWise step, cross-check the operation against
   `connectwise_catalog` and read the live record with a `connectwise_call`
   GET. For a desktop step, `observe_machine` (browser_scene or uia_tree)
   to see what the endpoint can actually see — never guess a selector.
3. **Name the cause**, with its evidence rung: wrong/blank rendered value,
   wrong CW reference, permission refused (the error carries CW's own status
   and message — read it), selector that matches nothing on the real screen,
   dead connection (`test_connection`), or a webhook that would never fire
   (`simulate_webhook` says why).
4. **Fix and prove.** Edit the graph, `validate_workflow`, then re-run the
   SAME test that failed — a desktop fix is proven with
   `test_step_on_machine` (real actuation: say what you're about to drive,
   prefer a test machine; the run scope is required). Then `update_workflow`.
5. **Report.** What failed, why, what changed, which test proved it, and who
   acts next — on a live playbook the fix lands staged behind a review URL,
   and the run is not fixed until a human applies it. An irreversible step
   that already fired (a sent note, an executed command) stays fired; say so
   rather than implying the revert covered it.
