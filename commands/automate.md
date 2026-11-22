---
description: Find automatable work and BUILD the automation as a draft in Orchard
argument-hint: "[what to automate, e.g. password resets]"
---

Find and build an automation for this MSP estate using the Orchard MCP server. Tool
names below are the server's own; your client namespaces them per server, so they may
surface as `mcp__…orchard__<tool>`. **You** are the author — Orchard supplies the rails
(connector catalog, graph validator, execution engine, approval gates); you supply the
graph. Orchard doesn't draft one for you; the nearest it comes is a ready-made
recipe (step 2).

1. **Find the work.** `find_automatable_work` (or `list_discoveries`). Pick the
   candidate matching "$ARGUMENTS", else the highest-impact `automatable: yes` one.
2. **Get the toolkit.** `get_workflow_toolkit` with that candidate's `discovery_id` —
   read the node catalog (types, PSA ops, field keys, branches), which connectors this
   tenant has wired, its evidence, the authoring rules and its `recipes`. If a recipe
   already does what was asked, offer `start_from_recipe` instead of authoring it by
   hand: it saves a draft whose trigger runs as a test run and posts nothing.
3. **Author the graph** `{nodes, edges}`:
   - exactly one trigger; pull per-run values from it with `{{ trigger.<key> }}`;
   - for values derived at run time, use a node's `ai_fields` so the engine fills them;
   - put ONE `human.approval` gate before the first outward/irreversible write;
   - end by writing the outcome back to the ticket (note, then close), on the
     tenant's own PSA node.
4. **Validate.** `validate_workflow` — fix any `errors` and re-validate until `valid`.
5. **Build.** `build_workflow` with `{name, graph, from_discovery_id}`. It saves a
   **DRAFT** and returns a review URL. (Needs the `build` scope on the connection —
   if you get an auth error, the operator must reconnect and approve building.)
6. **Report.** Tell the user what you built, the review URL, and that **they activate
   it in Orchard** — you build drafts, you never arm them.
