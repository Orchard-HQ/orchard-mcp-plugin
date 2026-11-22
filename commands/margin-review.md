---
description: The money view — agreement margin, unlogged work, and what automation is estimated to have returned
argument-hint: "[optional: client name to scope to]"
---

Review this MSP's automation economics using the Orchard MCP server. Tool names below
are the server's own; your client namespaces them per server, so they may surface as
`mcp__…orchard__<tool>`. Under per-seat billing, hours removed don't raise revenue —
they land on margin. That's the frame for the whole answer.

1. **Check your ground.** `estate_overview` — if no PSA is wired (its `connectors`),
   most of this is unavailable; say so plainly instead of producing a thin table that
   looks authoritative. Note the `freshness` of the `connectwise` source, which is the
   PSA sync whichever PSA it is.
2. **Pull the numbers** (scope to `$ARGUMENTS` via `client_id` where supported):
   - `agreement_margin` — fixed revenue minus tech labor at the loaded cost, worst
     margin first. This is the table. It is the books: someone who can't see them is
     refused, and if this connection is, say so rather than working around it.
   - `unlogged_work` — ticket work the Witness *observed* with no matching time
     entry. Leakage, priced. Different from margin: this is revenue never captured,
     not revenue eaten by labor.
   - `query_facts` with `fact: "psa_time"`, `measures: ["actual_hours", "entries"]`,
     `group_by: ["member", "company", "agreement"]` — hours by tech × company ×
     agreement. Who's carrying what. Its `coverage` names any day not built yet
     (today, always); say so rather than reading it as zero.
   - `savings_ledger` — capacity estimates for what activated automations have
     returned: completed runs against the manual baseline frozen when each went live.
     Gross estimates, not measured time or cash saved; read its method and where each
     rate comes from.
   - `list_discoveries` with `only_automatable: true` — the work still on the table.
3. **Answer four questions**, each with its number and its source:
   - **Which agreements are underwater**, and by how much?
   - **How much work is being done but never logged?**
   - **What is automation estimated to have returned?** Quote the ledger's figures
     as estimates, with its method and rates, and say they are gross: human effort
     and running costs are not deducted. If the ledger is empty, say it's empty and
     why (nothing activated, or activated with no frozen baseline: a gap, not zero).
   - **Where does the next hour of automation pay best?** Cross the worst-margin
     agreements against the automatable candidates — the overlap is the answer.
4. **Be honest about the measurement.** Neither number is a measured saving. The
   ledger's are capacity *estimates* for automation already running, from its runs
   against a baseline frozen at activation; discovery's are what work that is *not*
   automated takes a week now, from time observed on screens or logged in the PSA.
   They answer different questions: don't add the two into one total and present it
   as a fact. Label which is which.
