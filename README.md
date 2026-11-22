# Orchard Discovery: Claude Code plugin

Point Claude Code at an MSP estate. Orchard watches the technicians' activity stream
and the ticket and time records in the PSA (ConnectWise, Autotask, HaloPSA or Kaseya
BMS), and this plugin hands an agent the whole thing: the **recurring manual work that
shouldn't be manual**, ranked, priced, and mapped to the connector steps that would
automate it; the tickets, margins, fleet, signals and playbooks underneath it; the
rails to **build and edit the automations themselves**; and the Insights Studio
grammar for building live pages and tools from any shape of estate data.

This is the customer-facing surface of Orchard's own MCP server: the same capability
the platform runs on a schedule, callable by an agent, scoped to your tenant.

## What you get

- **`/find-automatable-work`**: scans the estate and returns ranked, prescriptive
  automation candidates (with time and dollars saved per week).
- **`/discovery-report [estate]`**: scans, then renders a branded, deck-ready **HTML
  Discovery Report** artifact, via the bundled `discovery-report` skill.
- **`/automate [what]`**: finds the work **and builds the automation**. The agent
  authors a workflow graph against Orchard's node catalog and validator and saves it
  as a **draft** in your tenant (you activate it), or sets up one of Orchard's
  ready-made recipes when one already does the job. Orchard supplies the rails and
  the agent does the authoring. Needs the `build` scope.
- **`/workflow-edit [playbook] — [change]`**: reads an existing playbook, proposes
  the change, shows you the node-level diff, validates, and saves a new version.
- **`/playbook-debug [playbook or run id]`**: takes a failing playbook (or the newest
  failed run), reproduces the failure with the cheapest test that proves it, fixes
  the cause, proves the fix, and saves it.
- **`/insights-page [request]`**: investigates the estate and builds or edits a
  complete, live page in Insights Studio: native tables/charts/timelines/maps,
  freeform scenes, networks, and sandboxed custom visuals. The model in this client
  authors the page, so direct creation does not require Orchard BYOK. Needs the
  `build` scope.
- **`/playbook-audit`**: every playbook checked for drift, fragility and dead weight:
  does the saved graph still validate, what keeps healing, what's active but never fires.
- **`/estate-brief [client]`**: a grounded brief on the estate: where the hours go,
  what needs attention, what's working, and the one thing to do next.
- **`/triage [severity]`**: open signals, failed runs and pending self-heals turned
  into a short ordered list of what a person should do now.
- **`/margin-review [client]`**: the money view: agreement margin, unlogged work, and
  the estimates of what automation has returned.

Four skills come along for the ride: `discovery-report` (the HTML artifact),
`workflow-authoring` (the graph grammar and the arming boundary, used by `/automate`
and `/workflow-edit`), `workflow-troubleshooting` (the evidence order, the test rungs
and the repair loop, used by `/playbook-debug`), and `insights-studio-authoring` (the
research, Visual IR, validation, and revision-safe save loop used by `/insights-page`).

- **MCP tools**, usable directly or by any agent. These are the server's own names;
  Claude Code namespaces tools per server, so installed from the marketplace they
  surface as `mcp__plugin_orchard-discovery_orchard__<tool>` (and as
  `mcp__orchard__<tool>` if you wire the server into `.mcp.json` by hand). A
  connection lists only the tools the workspace's products (Insights, Automations,
  Isaac's computer control add-on) and the signed-in person's role include.
  - **Orientation**: `estate_overview`: fleet and client counts, workflows by status,
    open signals, which connectors are wired, **how stale each source is**, the
    governance posture, and what your connection is allowed to do. Start here.
    `isaac_help` answers "how do I" questions about Orchard from its written help, and
    says so when the help doesn't cover one.
  - **Discovery**: `find_automatable_work` (a fresh scan of activity + PSA tickets;
    it upserts the candidates), `list_discoveries` (the current candidates, no rescan,
    each saying whether it came from the tickets or the computers).
  - **Fleet**: `list_machines`, `get_machine` (hardware and network inventory, the
    latest resource sample, security posture such as disk encryption, antivirus and
    EDR and local admins, and the installed apps matching a name), `list_clients` (or
    one client's review: what may be sent to the client, plus its renewal verdict and
    open recommendations for someone who can see the books), and `backup_state`: one
    computer's backups in Acronis Cyber Protect (each plan's last good backup, last
    run, next run, status and the last failure's reason), or a client's overview (how
    many computers are in each status and which have had no good backup in 3 days). It
    answers that Acronis isn't connected rather than guessing.
  - **Activity**: `activity_summary`, `activity_drilldown` (break any of its totals
    down by destination, category, app, person, day, machine or client, up to 365
    days, without paging events), `list_activity`, `query_activity_events` (the
    record-level work stream), `list_entities` (durable business records and who
    co-touched them), `list_rituals` (several real sittings of repeated work),
    `list_levers` (the mined manual work, each with the step sequence it was observed
    from rather than a re-fetched approximation), `list_process_candidates` (whole
    processes rather than one person's routine: records of one kind that the same
    roles handled, with their handoffs, waits and cycle times, scored by what each is
    worth fixing), `list_conversations` (chats with people outside the company, by who
    is on the other end, with the promises, chases and questions in them where chats
    are read; counts only, no names or text), `estate_graph` (org, process, network,
    or journey: how one ticket, invoice or quote moves from person to person and how
    long it waits between them), `get_insights`, and `get_outcomes` (what each team
    finished rather than where its time went: the clicks that commit work, each
    system's hours against what was finished in it, what followed AI use; teams only,
    never a person).
  - **Facts**: `query_facts`: one aggregate question over any day-grain fact (time
    by app, destination or person; screen time; network flows; tickets opened, closed,
    answered and inside SLA; logged PSA hours by member, company and agreement;
    workflow runs; AI spend; Isaac's usage), answered in the warehouse, with the days
    it is built through named rather than estimated. Billed amounts are refused to
    anyone who can't see the books. Call it with no fact for the catalogue of facts,
    dimensions and measures.
  - **PSA**: `list_tickets` (the synced tickets from ConnectWise, Autotask, HaloPSA
    or Kaseya BMS, with SLA risk on ConnectWise tickets), `get_ticket` (with its full
    timeline), `query_time_entries` (the underlying paginated time records),
    `agreement_margin`, `renewal_verdicts` (each client's call before its agreement
    renews: keep, reprice, true up, fix or exit review, with the notice date, the
    figures it came from and a draft message), and `unlogged_work`. Margin and renewal
    verdicts are the books, so they are refused to anyone who can't see them. Plus a
    live pair for each PSA: `connectwise_catalog` / `connectwise_call`,
    `autotask_catalog` / `autotask_call`, `halo_catalog` / `halo_call`, `bms_catalog`
    / `bms_call`. A catalog searches that PSA's vendored REST spec for the real paths,
    parameters and body (about 3,000 operations for ConnectWise and for Autotask, 1,500
    for HaloPSA, 435 for Kaseya BMS) and needs no connection. A call runs one
    operation against the live PSA, checked against the spec first. Reads work on any
    connection (Autotask's query POSTs and Kaseya BMS's search POSTs count as reads);
    every write needs the run scope, is audited, and can't be undone from here.
  - **Team and clients**: `teams` (the workspace's own teams and departments: who is
    on each, and the PSA territories, boards and clients they cover), `list_team`
    (Orchard logins, the PSA roster and the join between them, with unmapped techs
    named), `ticket_stats` (per person and for a team over a period: tickets opened,
    closed and reopened, first response and time to resolve, closed inside SLA, hours
    logged and billable, time off, each person against the team and the workspace's
    role expectations, with a monthly trend), `call_stats` (calls, talk time and
    after-call time per person, from calls captured on the desk or a phone system's
    call history; someone who neither runs the desk nor reviews calls reads only their
    own), and `client_spend` (per client: the services on each agreement, what it bills
    a month, what was invoiced, what changed, and the next renewal; it is the books, so
    it is refused to anyone who can't see them).
  - **Connections**: `connector_vendors` (the platforms Orchard connects, with how
    each signs in), `list_unconnected_tools` (tools the computers used in the last 30
    days that Orchard can connect and this workspace hasn't), `connector_setup_status`
    (what each connection and MCP server still needs, with the Settings link),
    `import_connector` (read an API from a link to its docs or spec; it previews, and
    saves only when asked), `connect_vendor` (save a connection to a vendor Orchard
    knows, by reference), and `add_mcp_server` (connect an outside MCP server for the
    workspace). Saving any of these takes an owner or admin and the build scope, and
    none takes a secret: a person adds the key at the link it returns.
    `connector_operation` describes one operation of a saved connection (its inputs,
    whether it changes data, a sample of its output) and calls nothing;
    `connector_call` runs one read of a saved connection live, and offers no writes.
    `connection_abilities` reads a connection's ability switches and Read only, and
    changes them for a workspace admin; `mcp_tool_policy` sets whether an outside MCP
    server's tool runs unasked, asks first or is off, for its owner or a workspace
    admin. Changing either needs the build scope.
  - **Tools and pages**: one document. A page shows data; a tool also runs playbooks
    for the people who don't build them, on a ticket or for a client, from the
    dashboard or the ConnectWise pod. Both are laid out in the Insights Studio
    grammar: view tiles (any renderer but custom) draw from Orchard data feeds or from
    what a playbook hands back, so the playbook is the page's backend.
    `get_tool_toolkit` (the Visual IR, renderer grammar, interface kit and the parts
    that run playbooks), `validate_tool` (check a whole tool without saving it),
    `list_tools`, `get_tool` (its tiles and data feeds, its playbooks' inputs and what
    each hands back, and its revision), and `save_tool` to make one or change one
    against the revision it was read at. Saves land in a draft its editors see until
    it is published. A tool over 30 KB is worked a part at a time: `tool_outline`,
    `tool_search` and `tool_read`, then `tool_edit` (replace text inside one part) or
    `tool_change_parts` (add, remove or move parts). `retheme_tool` swaps a tool's
    fixed colours for the theme's, in the draft. `check_tool_needs` checks every
    connection, playbook and switch a tool stands on, as you and as the people it is
    shared with, and names the fix; `test_tool` runs a saved tool's reads, actions and
    run tiles against real data with nothing changed outside Orchard; `sharing` reads
    or changes who may open, run or change a tool, page, data feed or connection;
    `source_rows` reads what a data feed last pulled from an outside connection.
    `preview_customer_page` shows a tool as a client will see it (needs the
    publish-public permission). `create_public_link` is listed but refuses here: a
    public link is made with a person's yes, through Isaac or the tool's Publish link
    in the dashboard. Saving, editing, testing, previewing and changing who may use
    something need the build scope. The model in this client does the authoring and
    needs no Orchard AI key; `create_insight_page_from_prompt` hands the research and
    composition to the workspace's BYOK-powered Studio agent instead (build scope and
    BYOK). The page tools' old names still answer for one more release, each as its
    new tool: `get_insight_page_toolkit`, `validate_insight_page`,
    `list_insight_pages`, `get_insight_page`, `create_insight_page` and
    `update_insight_page`.
  - **Authoring & editing**: `get_workflow_toolkit` (node catalog, wired connectors
    and MCP servers, Orchard's ready-made recipes, authoring rules),
    `find_connector_operations` (one app's operations in full, and whether you can
    call each now; calls nothing), `resolve_workflow_step` (a step said in plain
    words, turned into the app, the operation and the step to add; it asks when two
    apps fit, and uses the workspace's AI key), `validate_workflow` (validator +
    linter + the diff of a proposed edit; no save), `build_workflow` (save a graph as
    a draft), `start_from_recipe` (set up a recipe as a draft whose trigger runs as a
    test run, posting nothing until a person turns it on), `update_workflow` (edit an
    existing playbook), `set_workflow_status` (pause/stop/shelve one). All but the
    toolkit, `find_connector_operations` and `validate_workflow` need the build scope.
    A playbook hands an answer back with a "Hand back a result" step
    (transform.result): typed values declared in the graph, so `get_workflow` and
    `validate_workflow` return the declared result before it has ever run, and
    `get_run` and `run_workflow` return what the run handed back.
  - **Automation**: `list_workflows`, `get_workflow` (the current graph),
    `list_workflow_versions`, `get_workflow_evidence` (the Witness's receipts),
    `list_runs`, `get_run` (the per-step trail), `workflow_estate` (pulse and drift),
    `savings_ledger` (capacity estimates from completed runs against the manual
    baseline frozen at activation: estimates, not measured savings), `desk_work`
    (where automated work is fragile and where it waits: selector checks, steps that
    waited for a person and for how long, and agent sessions by outcome; counts only),
    `list_patterns`, `list_heals`, `list_documents` (SOPs).
  - **Running one**: `shadow_run_workflow` executes a playbook with every outward
    write provably suppressed, so you can see what it WOULD do before it does it
    (build scope). `run_workflow` executes it for real against this workspace's
    connected systems and returns the finished run; a step that can't be undone holds
    at an approval gate for a person (run scope). `revert_run` walks a finished run
    newest-step-first and undoes what can honestly be undone. Honestly is the
    operative word: an email that has been sent has no inverse, and revert says so
    rather than pretending (run scope).
  - **Diagnostics**: prove a step before a playbook depends on it.
    `test_workflow_node` (one step through an honesty ladder: reads run for real,
    writes render and execute nothing, desktop steps return the exact payload Orchard
    Desk would be handed), `sample_workflow_node` (side-effect-free steps for their
    real output shape), `observe_machine` / `get_observation` (what a computer can see:
    DOM scene, UIA tree, open windows; actuates nothing), `test_step_on_machine` /
    `get_step_test` (ONE desktop/terminal step on a real computer, no run around it,
    failure scene included; needs the run scope), `test_connection` (exercise a
    connection's stored secrets), `simulate_webhook` (payload validation + a shadow
    run + whether the real POST would land). All but the two readbacks and the step
    test need the build scope. Observing a computer and testing a step on one are
    refused while someone is at that keyboard or the workspace or client is supervised.
  - **The index**: the software this workspace uses, as a map. `index_apps` (the apps
    and sites it maps; start here), `index_surfaces` (an app's places),
    `index_controls` (a place's controls and the selectors the computers found them
    by), `index_find_control` (a control by part of its name), `index_path` (the
    fewest moves from one place to another), `index_copies` (where the values at a
    place come from and go), `index_coverage` (how many of your playbook steps it
    finds by control). It holds what recurred across the computers, never a person, a
    computer, a value or a window title, and it is refused to someone who sees only
    part of the workspace (a client's login, a client view, a member the team setting
    leaves out). One person's own layer, under your own visibility and your own desk
    unless you name another: `index_person` (where they work and when),
    `index_values` (the latest value per record and field, as a digest, never the
    value), `index_records` (the records they worked on), `index_sittings` (their
    visits to a place, with what each read and wrote).
  - **Computers**, with Isaac's computer control add-on: `start_agent_session`
    points Orchard's agent at a goal on one computer and runs on after the call
    returns; every step that changes the computer waits in its thread for a person to
    let it through, and you cannot approve one (build and run scopes).
    `list_agent_sessions`, `get_agent_session` (status, why it waits, the transcript)
    and `cancel_agent_session` need the build scope. `desks`, `look_at`, `do_step`,
    `run_command` and `fleet_run` are Isaac's own hands on a computer: they are
    listed, but over this connection they refuse, because they run inside an Isaac
    turn that waits for the computer. Ask Isaac in Orchard, or give
    `start_agent_session` the goal.
  - **Your own work**: what Isaac has prepared for you. `list_my_items`, `get_item`,
    `answer_item_question`, `accept_item` (applied as you, once every question is
    answered, with the same checks as the desk) and `dismiss_item` reach only your own
    items and only on a connection granted the `mcp:items` scope; a static token
    never reaches them. `ticket_emails` and `draft_ticket_reply` are listed but refuse
    here: a person's mailbox is read only by Isaac, for the person he works for.
  - **Governance**: `list_signals`, `governance_state`, `list_audit`.

## Setup: two lines, then sign in

In Claude Code:

```
/plugin marketplace add Orchard-HQ/orchard-mcp-plugin
/plugin install orchard-discovery@orchard
```

Then run any command (e.g. `/find-automatable-work`). The first call bounces you to
**Sign in with Orchard**: your browser opens, you approve the connection in the Orchard
dashboard while signed in as an owner/admin, and Claude Code receives a short-lived,
tenant-scoped access token automatically. **Nothing to configure, no token to paste.**
It refreshes itself. The approval screen lists what the connection asks for (read,
build, run) and Approve grants all of it. Without **build** the agent can read but not
author playbooks, tools or pages; without **run** it can't execute a playbook, write
to the PSA or drive a computer. The server is part of Isaac: a workspace without
Isaac gets a 404 from it.

<details><summary>Headless / CI (static token instead of the browser flow)</summary>

Make a token in the dashboard under **Settings → Connections → Advanced → API
tokens**, or mint one as an owner/admin:

```bash
curl -X POST "https://api.entertheorchard.ai/v1/mcp-tokens" \
  -H "Authorization: Bearer <operator-jwt>" -H "Content-Type: application/json" \
  -d '{"name": "claude-code"}'   # returns "token": mcp_<tenanthex>.<secret>, shown once
```

Then add `"headers": {"Authorization": "Bearer <that-token>"}` to the `orchard` server
entry in `.mcp.json`. Both auth methods are accepted. A token reads and builds; it
runs playbooks only if it was made with **May run playbooks** on (`"can_run": true`).
</details>

## Notes

- **Tenant-scoped and safe.** The token encodes your tenant; every tool is bound to
  your MSP's data by row-level security, never another tenant's and never the
  cross-tenant god-view. Inside the tenant a tool answers as the person who
  connected: a login held to one client sees that client, and what their role
  leaves out of Isaac is left out here too.
- **Writes are explicit and scoped.** `find_automatable_work` runs a scan, which
  upserts discovery candidates (an idempotent write). Authoring playbooks, saving
  tools and pages, setting up connections, test runs and the diagnostics that run a
  step require the `build` scope you approve at connect time; executing a playbook,
  writing to the PSA or driving a computer requires the separate `run` scope. Agent
  writes land in your own audit trail, actored as `mcp-agent`.
- **The arming boundary: an agent authors, a human arms.** This is enforced in the
  server, not asked for in a prompt:
  - `build_workflow` saves a **draft**. It cannot run until a person activates it.
    `start_from_recipe` does the same, and its trigger only records what it would
    have done until a person turns it on.
  - `update_workflow` on a draft adopts the edit. On a **live** playbook it appends
    the new version but leaves the workflow pointed at the one a human approved, so
    an agent can stage a change to a running automation, never make one. An
    owner/admin makes it live from the playbook's **More → Versions… → Adopt**, which
    makes that exact version current; a later human save supersedes a pending one.
  - `set_workflow_status` can only *lower* autonomy (pause, disable, archive). An
    agent can pull the brake on something misbehaving; it cannot start anything.
  - An agent session parks every step that changes the computer for a person to let
    through. The agent can't approve its own step.
- **A candidate becomes a draft, never a live automation.** `build_workflow` with
  `from_discovery_id` links the candidate and marks it accepted; in the dashboard,
  **Build it** on Insights → Recommendations makes the same kind of draft. Either way
  a person turns it on.
- **Revoke** a static token in the dashboard (**Settings → Connections → Advanced →
  API tokens**) or with `DELETE https://api.entertheorchard.ai/v1/mcp-tokens/{id}`
  (owner/admin). Changing your Orchard password signs out every app you connected
  with Sign in with Orchard.

## Development

There's no build step: this repo is markdown and JSON, and it installs straight from
GitHub. `python3 scripts/validate.py` (stdlib only) checks the manifests, the command
and skill frontmatter, and that no command names a tool the tool list above doesn't
document. CI runs it on every push; Orchard's control plane runs the same script with
the MCP server's real tool list, so a renamed tool fails there before it ships here.
