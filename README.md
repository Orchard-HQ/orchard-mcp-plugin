# Orchard Discovery — Claude Code plugin

Point Claude Code at an MSP estate. Orchard watches the technicians' activity stream
and the ConnectWise ticket/time corpus, and this plugin hands an agent the whole
thing: the **recurring manual work that shouldn't be manual** — ranked, priced, and
mapped to the connector steps that would automate it — plus the tickets, margins,
fleet, signals and playbooks underneath it, and the rails to **build and edit the
automations themselves**.

This is the customer-facing surface of Orchard's own MCP server: the same capability
the platform runs on a schedule, callable by an agent, scoped to your tenant.

## What you get

- **`/find-automatable-work`** — scans the estate and returns ranked, prescriptive
  automation candidates (with time and dollars saved per week).
- **`/discovery-report [estate]`** — scans, then renders a branded, deck-ready **HTML
  Discovery Report** artifact, via the bundled `discovery-report` skill.
- **`/automate [what]`** — finds the work **and builds the automation**: the agent
  authors a workflow graph against Orchard's node catalog + validator and saves it as
  a **draft** in your tenant (you activate it). Orchard supplies the rails; the agent
  does the authoring — no Orchard-side AI. Needs the `build` scope.
- **`/workflow-edit [playbook] — [change]`** — reads an existing playbook, proposes
  the change, shows you the node-level diff, validates, and saves a new version.
- **`/playbook-audit`** — every playbook checked for drift, fragility and dead weight:
  does the saved graph still validate, what keeps healing, what's active but never fires.
- **`/estate-brief [client]`** — a grounded brief on the estate: where the hours go,
  what needs attention, what's working, and the one thing to do next.
- **`/triage [severity]`** — open signals, failed runs and pending self-heals turned
  into a short ordered list of what a person should do now.
- **`/margin-review [client]`** — the money view: agreement margin, unlogged work, and
  what automation has measurably returned.

Two skills come along for the ride: `discovery-report` (the HTML artifact) and
`workflow-authoring` (the graph grammar and the arming boundary, used by `/automate`
and `/workflow-edit`).

- **MCP tools**, usable directly or by any agent. These are the server's own names;
  Claude Code namespaces tools per server, so installed from the marketplace they
  surface as `mcp__plugin_orchard-discovery_orchard__<tool>` (and as
  `mcp__orchard__<tool>` if you wire the server into `.mcp.json` by hand):
  - **Orientation** — `estate_overview`: fleet and client counts, workflows by status,
    open signals, which connectors are wired, **how stale each source is**, the
    governance posture, and what your connection is allowed to do. Start here.
  - **Discovery** — `find_automatable_work` (a fresh scan of activity + PSA),
    `list_discoveries` (the current candidates, no rescan).
  - **Authoring & editing** — `get_workflow_toolkit` (node catalog, wired connectors,
    authoring rules), `validate_workflow` (validator + linter + the diff of a proposed
    edit; no save), `build_workflow` (save a graph as a draft), `update_workflow` (edit
    an existing playbook), `set_workflow_status` (pause/stop/shelve one). The last three
    need the build scope.
  - **Automation** — `list_workflows`, `get_workflow` (the current graph),
    `list_workflow_versions`, `get_workflow_evidence` (the Witness's receipts),
    `list_runs`, `get_run` (the per-step trail), `workflow_estate` (pulse and drift),
    `savings_ledger` (measured savings vs. the frozen baseline), `list_patterns`,
    `list_heals`, `list_documents` (SOPs).
  - **Fleet** — `list_machines`, `get_machine` (with hardware inventory and live
    metrics), `list_clients` (or one client's impact rollup), `activity_summary`,
    `list_activity`, `estate_graph` (org / process / network), `get_insights`.
  - **PSA** — `list_tickets`, `get_ticket` (with its full timeline), `psa_workload`,
    `agreement_margin`, `unlogged_work`.
  - **Governance** — `list_signals`, `governance_state`, `list_audit`, `list_team`.

## Setup — two lines, then sign in

In Claude Code:

```
/plugin marketplace add Orchard-HQ/orchard-mcp-plugin
/plugin install orchard-discovery@orchard
```

Then run any command (e.g. `/find-automatable-work`). The first call bounces you to
**Sign in with Orchard**: your browser opens, you approve the connection in the Orchard
dashboard while signed in as an owner/admin, and Claude Code receives a short-lived,
tenant-scoped access token automatically. **Nothing to configure, no token to paste.**
It refreshes itself; revoke access any time from the dashboard. To let the agent build
automations, approve the **build** scope when prompted.

<details><summary>Headless / CI (static token instead of the browser flow)</summary>

Mint a long-lived per-tenant token and add it as a header:

```bash
curl -X POST "https://api.entertheorchard.ai/v1/mcp-tokens" \
  -H "Authorization: Bearer <operator-jwt>" -H "Content-Type: application/json" \
  -d '{"name": "claude-code"}'   # returns "token": mcp_<tenanthex>.<secret>, shown once
```

Then add `"headers": {"Authorization": "Bearer <that-token>"}` to the `orchard` server
entry in `.mcp.json`. Both auth methods are accepted.
</details>

## Notes

- **Tenant-scoped and safe.** The token encodes your tenant; every tool is bound to
  your MSP's data by row-level security — never another tenant's, never the
  cross-tenant god-view.
- **Writes are few, and scoped.** `find_automatable_work` runs a scan, which upserts
  discovery candidates (an idempotent write). Only three other tools write anything —
  `build_workflow`, `update_workflow`, `set_workflow_status` — and all three require
  the `build` scope you approve at connect time. Everything else is read-only. Agent
  writes land in your own audit trail, actored as `mcp-agent`.
- **The arming boundary: an agent authors, a human arms.** This is enforced in the
  server, not asked for in a prompt:
  - `build_workflow` saves a **draft**. It cannot run until a person activates it.
  - `update_workflow` on a draft adopts the edit. On a **live** playbook it appends
    the new version but leaves the workflow pointed at the one a human approved — so
    an agent can stage a change to a running automation, never make one.
  - `set_workflow_status` can only *lower* autonomy (pause, disable, archive). An
    agent can pull the brake on something misbehaving; it cannot start anything.
- **Accepting is an operator action.** Turning a candidate into a live workflow
  happens in the Orchard console (Discoveries → Accept) under owner/admin sign-in —
  deliberately not an agent-executable tool, since it creates an automation that can
  act on real systems.
- **Revoke** a token any time: `DELETE $ORCHARD_API_URL/v1/mcp-tokens/{id}` (operator auth).

## Development

There's no build step — this repo is markdown and JSON, and it installs straight from
GitHub. `python3 scripts/validate.py` (stdlib only) checks the manifests, the command
and skill frontmatter, and that no command names a tool the tool list above doesn't
document. CI runs it on every push; Orchard's control plane runs the same script with
the MCP server's real tool list, so a renamed tool fails there before it ships here.
