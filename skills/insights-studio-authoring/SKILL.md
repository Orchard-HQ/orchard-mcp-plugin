---
name: insights-studio-authoring
description: Investigate Orchard estate data and author or revise complete live Insights Studio pages through the Orchard MCP Visual IR tools. Use for dashboards, timelines, maps, charts, networks, activity views, custom visuals, or any request to create/edit a saved Insights page.
---

# Authoring Orchard Insights Studio pages

You own the investigation and the visual intent. Orchard owns tenant-scoped data
access, the versioned visual grammar, rendering, validation, persistence, and the
sandbox around custom code.

## Load contracts only when needed

Call `get_insight_page_toolkit` before authoring. It returns the current
VisualDocument schema, renderer contract, data-source contract, and the exact tools a
saved page may refresh. Do not reproduce or guess that grammar from this skill: the
toolkit is the runtime source of truth and keeps the ordinary MCP context small.

For an edit, call `list_insight_pages` to locate the page and `get_insight_page` to
read its full document, live data-source plan, and revision before changing anything.

## Research autonomously

Choose the reads that fit the operator's question. There is no mandatory sequence.
Start from a rollup when useful, but go into records, timelines, event streams, and
additional pages when a summary cannot establish the process. Application switching
is not a business process. Infer what happened from record-level evidence and preserve
uncertainty when the evidence is partial.

Keep the saved data plan purposeful. Each data source is a live Orchard MCP read with
an alias, tool, arguments, and reason. The page reruns those reads whenever it opens;
never paste source records into the document as a frozen substitute.

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

Call `validate_insight_page` with the complete document and data-source plan. Fix all
errors and repeat until valid.

- New page: `create_insight_page`.
- Existing page: `update_insight_page` with the `expected_revision` returned by
  `get_insight_page`. If Orchard reports a revision conflict, reopen the current page
  and reapply the requested change; never overwrite it blindly.

Direct creation and editing use the model in this MCP client, so they do not require
Orchard BYOK. They do require the connection's `build` scope. Use
`create_insight_page_from_prompt` only when the operator explicitly wants Orchard's
own autonomous Studio agent; that path uses the tenant's configured BYOK provider.

Finish with the saved page name, revision, and open URL. Call out missing/stale data
or assumptions that materially affect what the page says.
