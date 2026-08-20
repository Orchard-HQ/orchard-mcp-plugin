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

1. Call `get_insight_page_toolkit` to load the current visual and data-source contract.
2. Investigate the request autonomously with the relevant read-only Orchard tools.
   Open underlying records and paginate when summaries cannot establish what is
   happening. There is no prescribed query sequence.
3. Design a complete page, normally with multiple tiles. Prefer native renderers;
   use a freeform scene when the view needs an original composition, and custom code
   only when neither can express it.
4. Call `validate_insight_page` and correct every error.
5. New page: call `create_insight_page`. Existing page: locate it with
   `list_insight_pages`, read it with `get_insight_page`, preserve its current
   revision, and call `update_insight_page` with `expected_revision`.
6. Return the saved page name, revision, and Orchard URL. State any important data
   gaps or uncertainty plainly.

Direct create/update require the connection's `build` scope but do not require an
Orchard BYOK key: the model in this client already did the authoring.
