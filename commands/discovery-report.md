---
description: Generate a branded, deck-ready Discovery Report for an MSP estate
argument-hint: "[estate name for the title]"
---

Generate an Orchard **Discovery Report** for this MSP estate using the Orchard MCP
server. Tool names below are the server's own; your client namespaces them per
server, so they may surface as `mcp__…orchard__<tool>`.

1. Call `find_automatable_work` to run a fresh scan and get the ranked
   automation candidates. (If the user only wants the current list without
   rescanning, call `list_discoveries` instead.)
2. Use the **discovery-report** skill to render the results as a branded HTML report
   and publish it as an artifact. Use `$ARGUMENTS` as the estate name in the title
   if provided; otherwise infer it from context or ask.
3. After publishing, give the user the artifact link and a 3-bullet summary of the
   top automatable work — hours, the clearest "yes", and the honest caveat.

Keep it truthful: if the estate is thin, the report should say so. The credibility
is that the engine finds the work where it exists and admits where it doesn't.
