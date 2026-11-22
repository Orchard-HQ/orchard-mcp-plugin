---
description: Investigate the estate and build or edit a live multi-tile Insights Studio page
argument-hint: "[the operating view to build, or page name — requested edit]"
---

Build or edit an Orchard Insights Studio page for "$ARGUMENTS" using the Orchard MCP
server. Use the **insights-studio-authoring** skill. Tool names below are the server's
own; your client may namespace them as `mcp__…orchard__<tool>`.

You are the researcher and visual author. Orchard supplies tenant-scoped data tools,
the Visual IR, validation, rendering, live refresh, and persistence. Do not delegate
back to another model unless the user explicitly asks to use Orchard's BYOK agent.

1. Call `get_tool_toolkit` to load the current visual and data-source contract.
2. Investigate the request autonomously with the relevant read-only Orchard tools.
   Open underlying records and paginate when summaries cannot establish what is
   happening. There is no prescribed query sequence.
3. Design a complete page, normally with multiple tiles. Prefer native renderers;
   use a freeform scene when the view needs an original composition, and custom code
   only when neither can express it.
4. Call `validate_tool` with the `document` and its `data_sources`, and correct
   every error.
5. New page: call `save_tool` with the `document` and `data_sources` and no
   `tool_id`. Existing page: locate it with `list_tools`, read it with `get_tool`,
   keep its `revision`, and call `save_tool` with its `tool_id`, `expected_revision`,
   the changed `document` and its `data_sources`. A page over 30 KB is changed part
   by part instead: `tool_outline`, `tool_search`, `tool_read`, then `tool_edit`.
6. Call `check_tool_needs` with the `tool_id` and pass on any fix or ask it returns.
7. Return the saved page name, `tool_id`, revision, whether it is still a draft, and
   its Orchard path. A save is a draft its editors alone see; publish it
   (`publish: true`) only when the user asks. State any important data gaps or
   uncertainty plainly.

Saving requires the connection's `build` scope but does not require an Orchard BYOK
key: the model in this client already did the authoring.
