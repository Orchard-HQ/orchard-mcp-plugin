---
name: workflow-authoring
description: Author and edit Orchard workflow graphs safely — the sequence, the templating rules, and the arming boundary. Use whenever building a new Orchard automation or changing an existing playbook via the Orchard MCP tools (get_workflow_toolkit, validate_workflow, build_workflow, update_workflow).
---

# Authoring Orchard workflows

You are the author. Orchard supplies the rails — the connector catalog, the graph
validator, the execution engine, the approval gates — and you supply the graph. It
never drafts one for you.

**Never invent the catalog.** Node types, ConnectWise operations, config field keys
and branch names all come from `get_workflow_toolkit` at run time, per tenant. A
config key you made up doesn't fail loudly — it fails *silently* at run time, on a
live system. Read the toolkit first, every time.

## The sequence

Build and edit are the same loop with a different last step.

1. **Orient.** `estate_overview` — is ConnectWise wired? Is the estate paused? What's
   the autonomy ceiling? Can this connection even build (the `mcp:build` scope)?
   A supervised estate holds every outward write for approval no matter what your
   graph says, and that changes what a good graph looks like.
2. **Ground it in evidence.** `list_discoveries` / `find_automatable_work` for the
   work itself; `list_tickets`, `list_patterns` or `activity_summary` when you need
   to see the raw shape rather than trust the summary.
3. **Get the toolkit.** `get_workflow_toolkit` (pass `discovery_id` when you have
   one) — the catalog, the wired connectors, the authoring rules, the evidence.
4. **Read what exists** — editing only. `get_workflow` returns the current graph,
   its status, its triggers and the linter's warnings. Never edit a graph you
   haven't read.
5. **Author the change.**
6. **Validate.** `validate_workflow`. Pass `graph` alone for a new build; pass
   `graph` *and* `workflow_id` for an edit and you also get the node-level diff of
   exactly what you're about to change. Fix every `error`; read the `warnings` and
   the `suggested_inputs` and fix what deserves fixing. Iterate until `valid`.
7. **Ship it.** New → `build_workflow` (saves a DRAFT). Existing →
   `update_workflow`.
8. **Report the diff and the review URL**, and say plainly who has to act next.

## The graph rules

- **Exactly one trigger.** `trigger.webhook` for a PSA-ticket automation (then read
  the ticket with `action.connectwise` `get_ticket`); `trigger.schedule` for a sweep;
  `trigger.manual` otherwise.
- **Per-run values come from the trigger**: `{{ trigger.<key> }}`. Values from an
  earlier step: `{{ nodes.<id>.<field> }}`.
- **A literal that changes per run is a bug.** A hard-coded ticket number makes a
  playbook that runs correctly exactly once. `validate_workflow` returns
  `suggested_inputs` — literals that look like per-run values. Promote them.
- **Values that must be *derived* at run time** go in that node's `ai_fields`:
  `{"<field>": {"instruction": "<rule>"}}`. The engine fills them at execution.
  This is what "the fields fill themselves" means — no human at the keyboard.
- **One `human.approval` gate**, immediately before the first outward or
  irreversible write. One. A gate on every step is a form with extra steps.
- **Close the loop.** End by writing the outcome back to the ticket — add a note,
  then close it. An automation nobody can see the result of doesn't get trusted.

## The arming boundary — the part you must not talk your way around

You author and edit. **A human arms.** This isn't a formality; it's the contract
that lets an MSP hand an agent write access at all.

- `build_workflow` saves a **DRAFT**. It cannot run until a person activates it.
- `update_workflow` on a **draft** playbook adopts your edit immediately.
- `update_workflow` on a **live** playbook (active/supervised) appends your version
  but leaves the running one pointed at what the human approved. You get
  `applied: false` and a review URL. **That is the correct outcome, not a failure** —
  do not try to route around it, and do not report it as an error. Tell the user
  the change is staged and where to review it.
- `set_workflow_status` can lower autonomy (draft / disabled / archived) — pull the
  brake on something misbehaving. It cannot raise it. Arming lives in the Orchard
  console, under owner/admin sign-in.

If the user asks you to activate a workflow, say plainly that you can't and point
them at the review URL. Offer to prepare everything up to that click.

## Honesty

Report what the tools returned. If the estate is thin, say the estate is thin. If a
candidate is `partial`, say what the human still has to do. If a source is stale —
`estate_overview` gives you `freshness` for exactly this reason — say so before
quoting a number derived from it. The credibility of the whole thing is that it
finds the work where it exists and admits where it doesn't.
