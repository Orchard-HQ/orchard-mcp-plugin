---
description: Edit an existing Orchard playbook — read it, propose the change, validate, save
argument-hint: "[playbook name or id] — [what to change]"
---

Change an existing Orchard automation using the Orchard MCP server. Tool names below
are the server's own; your client namespaces them per server, so they may surface as
`mcp__…orchard__<tool>`. Use the **workflow-authoring** skill for the graph grammar
and the arming boundary.

Request: **$ARGUMENTS**

1. **Find the playbook.** `list_workflows`. Match "$ARGUMENTS" by name or id. If
   nothing matches or several do, show the list and ask — don't guess which live
   automation to edit.
2. **Read it.** `get_workflow` — the current graph, its status, its triggers, the
   linter's warnings. Note whether `is_live` is true: that decides what step 6 can do.
3. **Get the toolkit.** `get_workflow_toolkit` — node types, ConnectWise ops, config
   field keys, and which connectors this tenant actually has wired. Never edit using
   a field key you didn't read here.
4. **Author the new graph.** Change as little as possible: keep node ids stable so
   the diff reads as the edit you intended, not a rewrite.
5. **Validate and diff.** `validate_workflow` with **both** `graph` and
   `workflow_id`. Show the user the `diff` and any `warnings` *before* saving. Fix
   every error and re-validate until `valid`.
6. **Save.** `update_workflow` with `workflow_id`, `graph`, and a `note` that says
   **why** — the note lands in the immutable version history and is what someone
   reads six months from now.
7. **Report honestly**, using what came back:
   - `applied: true` → the playbook wasn't live, so the edit is in effect. Say which
     version it is.
   - `applied: false` → **this is the expected outcome for a live playbook, not a
     failure.** The version is staged; the automation still runs the human-approved
     one. Give the review URL and say an operator adopts it in Orchard.

If the user actually wants to *stop* a misbehaving playbook rather than fix it,
`set_workflow_status` can pause (`draft`), stop (`disabled`) or shelve (`archived`)
it. It cannot arm one — that stays an operator action.
