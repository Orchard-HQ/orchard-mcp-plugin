# Orchard Discovery — Claude Code plugin

Point Claude Code at an MSP estate. Orchard watches the technicians' activity stream
and the ConnectWise ticket/time corpus, and this plugin hands an agent the whole
thing: the **recurring manual work that shouldn't be manual** — ranked, priced, and
mapped to the connector steps that would automate it — plus the tickets, margins,
fleet, signals and playbooks underneath it, the rails to **build and edit the
automations themselves**, and an open visual grammar for creating complete, live
Insights pages from any shape of estate data.

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
- **`/insights-page [request]`** — investigates the estate and builds or edits a
  complete, live page in Insights Studio: native tables/charts/timelines/maps,
  freeform scenes, networks, and sandboxed custom visuals. The model in this client
  authors the page, so direct creation does not require Orchard BYOK. Needs the
  `build` scope.
- **`/playbook-audit`** — every playbook checked for drift, fragility and dead weight:
  does the saved graph still validate, what keeps healing, what's active but never fires.
- **`/estate-brief [client]`** — a grounded brief on the estate: where the hours go,
  what needs attention, what's working, and the one thing to do next.
- **`/triage [severity]`** — open signals, failed runs and pending self-heals turned
  into a short ordered list of what a person should do now.
- **`/margin-review [client]`** — the money view: agreement margin, unlogged work, and
  what automation has measurably returned.

Three skills come along for the ride: `discovery-report` (the HTML artifact),
`workflow-authoring` (the graph grammar and the arming boundary, used by `/automate`
and `/workflow-edit`), and `insights-studio-authoring` (the research, Visual IR,
validation, and revision-safe save loop used by `/insights-page`).

- **MCP tools**, usable directly or by any agent. These are the server's own names;
  Claude Code namespaces tools per server, so installed from the marketplace they
  surface as `mcp__plugin_orchard-discovery_orchard__<tool>` (and as
  `mcp__orchard__<tool>` if you wire the server into `.mcp.json` by hand):
  - **Orientation** — `estate_overview`: fleet and client counts, workflows by status,
    open signals, which connectors are wired, **how stale each source is**, the
    governance posture, and what your connection is allowed to do. Start here.
  - **Discovery** — `find_automatable_work` (a fresh scan of activity + PSA),
    `list_discoveries` (the current candidates, no rescan).
  - **Insights Studio** — `get_insight_page_toolkit` (the on-demand Visual IR and
    renderer grammar), `validate_insight_page`, `list_insight_pages`,
    `get_insight_page`, `create_insight_page`, and `update_insight_page`. Direct
    creation uses the model already running in this client and needs no Orchard AI
    key; `create_insight_page_from_prompt` delegates the research and composition to
    the tenant's BYOK-powered Orchard Studio agent. Create/update need the build scope.
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
  - **Running one** — `shadow_run_workflow` executes a playbook with every outward
    write provably suppressed, so you can see what it WOULD do before it does it
    (build scope). `run_workflow` executes it for real against this workspace's
    connected systems and returns the finished run (run scope). `revert_run` walks
    a finished run newest-step-first and undoes what can honestly be undone —
    honestly being the operative word: an email that has been sent has no inverse,
    and revert says so rather than pretending (run scope).
  - **Fleet** — `list_machines`, `get_machine` (with hardware inventory and live
    metrics), `list_clients` (or one client's impact rollup), `activity_summary`,
    `list_activity`, `query_activity_events` (the record-level work stream),
    `list_entities` (durable business records and who co-touched them),
    `list_rituals` (several real sittings of repeated work), `estate_graph` (org /
    process / network), `get_insights`, `list_levers` (the mined manual work, each
    with the step sequence it was observed from rather than a re-fetched
    approximation).
  - **PSA** — `list_tickets`, `get_ticket` (with its full timeline), `psa_workload`,
    `query_time_entries` (the underlying paginated PSA records), `agreement_margin`,
    `unlogged_work`. Plus the live pair: `connectwise_catalog` (search the vendored
    CW REST spec — ~3,000 operations with their real paths, parameters and required
    fields) and `connectwise_call` (execute one operation against the live PSA,
    spec-validated first; GET on any connection, writes need the run scope and are
    audited).
  - **Diagnostics** — prove a step before a playbook depends on it:
    `test_workflow_node` (one step through an honesty ladder — reads run for real,
    writes render and execute nothing, desktop steps return the exact watcher
    payload), `sample_workflow_node` (side-effect-free steps for their real output
    shape), `observe_machine` / `get_observation` (what an endpoint can see — DOM
    scene, UIA tree, open windows — actuates nothing), `test_step_on_machine` /
    `get_step_test` (ONE desktop/terminal step on a real endpoint, no run around
    it, failure scene included; needs the run scope), `test_connection` (exercise
    a connection's stored secrets), `simulate_webhook` (payload validation + a
    shadow run + whether the real POST would land).
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
automations or Studio pages, approve the **build** scope when prompted.

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
- **Writes are explicit and scoped.** `find_automatable_work` runs a scan, which
  upserts discovery candidates (an idempotent write). Workflow authoring and Studio
  page creation/editing require the `build` scope you approve at connect time;
  executing a workflow or mutating ConnectWise requires the separate `run` scope.
  Agent writes land in your own audit trail, actored as `mcp-agent`.
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
