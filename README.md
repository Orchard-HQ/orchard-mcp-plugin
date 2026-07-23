# Orchard Discovery — Claude Code plugin

Run Orchard's automation-discovery engine against an MSP estate from Claude Code.
Orchard watches the technicians' activity stream and the ConnectWise ticket/time
corpus and surfaces the **recurring, manual work that shouldn't be manual** —
ranked, priced, and mapped to the connector steps that would automate it.

This plugin is the first customer-facing use of Orchard's own MCP server: the same
discovery capability the platform runs on a schedule, callable by an agent.

## What you get

- **Slash command `/find-automatable-work`** — scans the estate and returns ranked,
  prescriptive automation candidates (with time and dollars saved per week).
- **Slash command `/discovery-report [estate]`** — scans, then renders a branded,
  deck-ready **HTML Discovery Report** artifact (the same format as the Beacon /
  Diamond / Titan field reports), via the bundled `discovery-report` skill.
- **Slash command `/automate [what]`** — finds the work **and builds the automation**:
  the agent authors a workflow graph against Orchard's node catalog + validator and
  saves it as a **draft** in your tenant (you activate it). Orchard supplies the rails;
  the agent does the authoring — no Orchard-side AI. Needs the `build` scope (approve it
  at connect time).
- **MCP tools** (namespaced `mcp__orchard__*`), usable directly or by any agent:
  - `find_automatable_work` — run a fresh discovery scan (activity + PSA) and return candidates.
  - `list_discoveries` — read the current candidates without rescanning (`only_automatable` optional).
  - plus Orchard's read-only estate tools: `list_machines`, `get_machine`, `list_clients`,
    `list_workflows`, `list_runs`, `get_run`, `activity_summary`, `list_activity`.

## Setup

1. **Point at your Orchard API** — the one environment variable Claude Code expands into `.mcp.json`:

   ```bash
   export ORCHARD_API_URL="https://api.entertheorchard.ai"   # your Orchard API origin
   ```

2. **Install the plugin** (from a marketplace that lists it, or a local path), then in Claude Code:

   ```
   /find-automatable-work
   ```

3. **Sign in with Orchard.** The first call returns a 401 that advertises Orchard's OAuth
   server; Claude Code opens your browser, you approve the connection **in the Orchard
   dashboard while signed in as an owner/admin**, and it receives a short-lived,
   tenant-scoped access token automatically — no token to copy or paste. It refreshes
   itself; revoke access any time from the dashboard.

<details><summary>Alternative: a static token (no browser)</summary>

For headless use, mint a long-lived per-tenant token and set it as a header instead:

```bash
curl -X POST "$ORCHARD_API_URL/v1/mcp-tokens" \
  -H "Authorization: Bearer <operator-jwt>" -H "Content-Type: application/json" \
  -d '{"name": "claude-code"}'   # returns "token": mcp_<tenanthex>.<secret>, shown once
```

Then add `"headers": {"Authorization": "Bearer ${ORCHARD_MCP_TOKEN}"}` to the server
entry in `.mcp.json` and export `ORCHARD_MCP_TOKEN`. Both auth methods are accepted.
</details>

## Notes

- **Tenant-scoped and safe.** The token encodes your tenant; every tool is bound to
  your MSP's data by row-level security — never another tenant's, never the
  cross-tenant god-view.
- **One tool writes.** `find_automatable_work` runs a scan, which upserts discovery
  candidates (an idempotent write). Everything else is read-only.
- **Accepting is an operator action.** Turning a candidate into a live workflow
  happens in the Orchard console (Discoveries → Accept) under owner/admin sign-in —
  deliberately not an agent-executable tool, since it creates an automation that can
  act on real systems.
- **Revoke** a token any time: `DELETE $ORCHARD_API_URL/v1/mcp-tokens/{id}` (operator auth).
