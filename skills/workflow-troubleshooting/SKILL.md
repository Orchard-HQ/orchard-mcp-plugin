---
name: workflow-troubleshooting
description: Diagnose and fix a misbehaving Orchard playbook step by step — the evidence order, the test rungs, and the repair loop. Use whenever a workflow failed, a ConnectWise step errors, a desktop step misses its target, or a webhook never fires, driven through the Orchard MCP diagnostics tools (test_workflow_node, observe_machine, test_step_on_machine, connectwise_catalog, test_connection, simulate_webhook).
---

# Troubleshooting Orchard workflows

A failed run is a claim about one step. Your job is to reproduce that one step,
in the cheapest way that still proves something, and fix the cause — not to
re-run the playbook until it goes green.

**Cheapest honest test first.** Every rung below is more expensive and more
real than the one above it. Climb only as far as the diagnosis needs:

1. `get_run` — the per-step trail. The failing step's `input` is the RENDERED
   config: a blank where a `{{ ref }}` should have resolved is a diagnosis in
   itself (and `_unresolved` names the token).
2. `test_workflow_node` with `context_run_id` pointing at the failed run — the
   same step, the same data, no side effects for writes. Reads run for real;
   a write returns exactly what it WOULD have sent. Most failures die here:
   the rendered payload shows the wrong board id, the empty ticket number, the
   condition taking the other branch.
3. For ConnectWise steps: `connectwise_catalog` for what the operation really
   wants, then `connectwise_call` with a GET to see the live record the step
   would touch. A 403 here is a permissions diagnosis, not a workflow bug —
   the error carries CW's own status and message now; read it, don't guess.
4. For desktop steps: `observe_machine` FIRST (browser_scene / uia_tree — it
   actuates nothing and shows the control names that exist right now), then,
   only when you need proof the step lands, `test_step_on_machine` — one real
   step on a real endpoint. It drives the actual desktop: say what you are
   about to drive before you drive it, and prefer a test machine.
5. For auth: `test_connection`. For webhooks: `simulate_webhook` — it also
   tells you whether the REAL delivery would land (trigger present, enabled,
   playbook armed), which is the answer when "the webhook never fires."

## The repair loop

Diagnose → edit → validate → re-test the SAME rung that failed → then
`update_workflow`. The arming boundary holds throughout (see the
workflow-authoring skill): on a live playbook your fix lands as a staged
version with a review URL, and that is the correct outcome, not a failure.

- A failing desktop selector: the scene from `get_step_test` (or a failed
  run's step result) lists what the watcher actually saw. Fix the selector to
  match the scene, prove it with `test_step_on_machine`, then edit the graph.
- Never fix by widening: a step that fails on a missing required field gets
  the field, not a retry bump. `retries` on a step is for flaky transport,
  not for wrong configuration.
- One variable at a time. A test that changes the config overlay AND borrows
  a different run's context has proved nothing when it passes.

## Honesty

Report which rung each conclusion came from. "The rendered payload shows X"
(rung 2) and "the live endpoint answered X" (rung 3+) are different strengths
of evidence — say which you have. A step you could not test (machine offline,
scope missing) is UNTESTED; say that, never infer it works. If the fix is
staged behind a review URL, the run is not fixed until a human applies it —
end by saying who has to act next.
