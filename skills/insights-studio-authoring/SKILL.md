---
name: insights-studio-authoring
description: Investigate Orchard estate data and author or revise complete live Insights Studio pages through the Orchard MCP Visual IR tools. Use for dashboards, timelines, maps, charts, networks, activity views, custom visuals, or any request to create/edit a saved Insights page.
---

# Authoring Orchard Insights Studio pages

You own the investigation and the visual intent. Orchard owns tenant-scoped data
access, the versioned visual grammar, rendering, validation, persistence, and the
sandbox around custom code.

A page and a tool are one document in Orchard, so pages are made and changed with
the tool set's calls. A page is views alone; a request for forms, buttons, tables to
act on or playbooks to run is a tool, built as tiles from the toolkit's `kit`, not as
a page document.

## Load contracts only when needed

Call `get_tool_toolkit` before authoring. It returns the current VisualDocument
schema, renderer contract, data-source contract, and the exact tools a saved page may
refresh. Do not reproduce or guess that grammar from this skill: the toolkit is the
runtime source of truth and is large, so it is read when needed and not otherwise.

For an edit, call `list_tools` to locate the page and `get_tool` with its `tool_id`
to read it before changing anything: its `name`, `description` and `tiles` are the
document, its `data` is the data-source plan, and `revision` is what you send back.
`get_tool` reads the draft when you may edit the page. A page over 100 KB comes back
as an outline, and one over 30 KB is better worked part by part: `tool_outline`,
`tool_search` to find the part, `tool_read` to read it whole, then `tool_edit` to
replace text inside it or `tool_change_parts` to add, remove or move parts.

## Research autonomously

Choose the reads that fit the operator's question. There is no mandatory sequence.
Start from a rollup when useful, but go into records, timelines, event streams, and
additional pages when a summary cannot establish the process. Application switching
is not a business process. Infer what happened from record-level evidence and preserve
uncertainty when the evidence is partial.

Keep the saved data plan purposeful. Each data source is a live read with an alias,
tool, arguments, and reason: a read-only Orchard tool from the toolkit's catalog,
`call_operation` for a read of a connected system, or a read tool on an MCP server the
person has connected. The page reruns those reads whenever it opens; never paste
source records into the document as a frozen substitute. A read on the person's own
sign-in makes the page theirs alone.

## Compose the whole page

Build a page, not one giant fragment. Normally create multiple tiles with a clear
editorial hierarchy and useful span variation.

- Prefer native renderers for metrics, narrative, tables, timelines/Gantt views,
  standard charts, maps, and networks. Orchard supplies responsiveness,
  accessibility, interactions, and empty states.
- Use `scene` for original mark-based compositions that do not fit a named chart.
  It is the abstract visual surface, not a synonym for Mermaid.
- Use `custom` only when native renderers and scene cannot express the request. Keep
  it dependency-free and inside the toolkit's sandbox contract.
- Every tile must name exactly the aliases it uses. Every `spec.source` must be one
  of those aliases.
- Use ordinary business language. Do not expose implementation language, internal
  field names, or unsupported certainty to the operator.

## Validate, save, and revise safely

Call `validate_tool` with the complete `document` and its `data_sources`. Fix all
errors and repeat until valid.

- New page: `save_tool` with the `document` and `data_sources`, and no `tool_id`.
- Existing page: `save_tool` with its `tool_id`, the `expected_revision` that
  `get_tool` returned, the changed `document` and its `data_sources`. If Orchard
  reports a revision conflict, read the page again and reapply the requested change;
  never overwrite it blindly.

A save is a draft its editors alone see. Publish (`publish: true`) only when the
operator asks for it. Then call `check_tool_needs` with the `tool_id` and pass on any
fix or ask it returns.

Direct creation and editing use the model in this MCP client, so they do not require
Orchard BYOK. They do require the connection's `build` scope. Use
`create_insight_page_from_prompt` only when the operator explicitly wants Orchard's
own autonomous Studio agent; that path uses the tenant's configured BYOK provider.

Finish with the saved page name, `tool_id`, revision, whether it is still a draft, and
its path. Call out missing/stale data or assumptions that materially affect what the
page says.
