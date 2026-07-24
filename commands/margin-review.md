---
description: The money view — agreement margin, unlogged work, and what automation has actually returned
argument-hint: "[optional: client name to scope to]"
---

Review this MSP's automation economics using the Orchard MCP server. Tool names below
are the server's own; your client namespaces them per server, so they may surface as
`mcp__…orchard__<tool>`. Under per-seat billing, hours removed don't raise revenue —
they land on margin. That's the frame for the whole answer.

1. **Check your ground.** `estate_overview` — if ConnectWise isn't wired, most of
   this is unavailable; say so plainly instead of producing a thin table that looks
   authoritative. Note the `freshness` of the `connectwise` source.
2. **Pull the numbers** (scope to `$ARGUMENTS` via `client_id` where supported):
   - `agreement_margin` — fixed revenue minus tech labor at the loaded cost, worst
     margin first. This is the table.
   - `unlogged_work` — ticket work the Witness *observed* with no matching time
     entry. Leakage, priced. Different from margin: this is revenue never captured,
     not revenue eaten by labor.
   - `psa_workload` — hours by tech × company × agreement. Who's carrying what.
   - `savings_ledger` — what activated automations have measurably returned against
     the manual baseline frozen when each went live.
   - `list_discoveries` with `only_automatable: true` — the work still on the table.
3. **Answer four questions**, each with its number and its source:
   - **Which agreements are underwater**, and by how much?
   - **How much work is being done but never logged?**
   - **What has automation already returned?** If the ledger is empty, say it's empty
     and why (nothing activated, or activated with no frozen baseline) — never
     substitute an estimate for a measurement.
   - **Where does the next hour of automation pay best?** Cross the worst-margin
     agreements against the automatable candidates — the overlap is the answer.
4. **Be honest about the measurement.** Savings on the ledger are measured against a
   frozen baseline; discovery numbers are *estimates* from observed frequency. Don't
   add the two into one total and present it as a fact. Label which is which.
