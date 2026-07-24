#!/usr/bin/env python3
"""Validate this plugin: manifests, commands, skills, and the documented tool surface.

Stdlib only, no install step — CI runs it on every push, and it's the same check the
control-plane repo drives from `make plugin`, which passes the tools its MCP server
actually exposes:

    python3 scripts/validate.py                                  # structure + self-consistency
    python3 scripts/validate.py --tools a,b,c --endpoint /v1/mcp # + the server's truth

The tool vocabulary is the README's "MCP tools" bullet — the plugin's declared surface.
Commands may only name tools from it, and with --tools the README may not claim a tool
the server doesn't have. That's what keeps a rename from shipping a plugin that calls a
dead tool. (Anchored on the visible bullet, not a marker comment: the README is customer
-facing and shouldn't carry scaffolding.)"""

from __future__ import annotations

import argparse
import difflib
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

# The server's own name, and the namespaced spellings clients give it (Claude Code
# prefixes per server: mcp__orchard__x wired by hand, mcp__plugin_<plugin>_orchard__x
# when installed from the marketplace).
TOOL_REF = re.compile(r"mcp__(?:plugin_[\w-]+_)?orchard__(\w+)")
BACKTICKED = re.compile(r"`([a-z][a-z0-9_]*)`")
# The "- **MCP tools**…" bullet and everything nested under it, i.e. up to the next
# top-level bullet or heading.
TOOL_BLOCK = re.compile(r"^- \*\*MCP tools\*\*.*?(?=^- |^#|\Z)", re.S | re.M)

failures: list[str] = []
warnings: list[str] = []


def fail(msg: str) -> None:
    failures.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


def load_json(path: pathlib.Path) -> dict:
    try:
        return json.loads(path.read_text())
    except FileNotFoundError:
        fail(f"missing {path.relative_to(ROOT)}")
    except json.JSONDecodeError as exc:
        fail(f"{path.relative_to(ROOT)}: invalid JSON — {exc}")
    return {}


def frontmatter(path: pathlib.Path) -> dict[str, str]:
    """Parse the leading `---` block. Flat `key: value` only — that's all we ship."""
    text = path.read_text()
    if not text.startswith("---"):
        fail(f"{path.relative_to(ROOT)}: no YAML frontmatter")
        return {}
    _, block, _ = text.split("---", 2)
    out = {}
    for line in block.strip().splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            out[key.strip()] = value.strip().strip("\"'")
    return out


def documented_tools(readme: str) -> set[str]:
    block = TOOL_BLOCK.search(readme)
    if not block:
        fail("README.md: no '- **MCP tools**' bullet — that list is what tools are checked against")
        return set()
    return set(BACKTICKED.findall(block.group(0)))


def check_manifests(endpoint: str | None) -> dict:
    manifest = load_json(ROOT / ".claude-plugin" / "plugin.json")
    for key in ("name", "description"):
        if not manifest.get(key):
            fail(f"plugin.json: missing '{key}'")
    # `version` is deliberately ABSENT. Claude Code resolves a plugin's version from
    # plugin.json, then the marketplace entry, then the git commit SHA — and that
    # version is the cache key for updates. With an explicit version, users receive
    # changes ONLY when it's bumped: pushing commits without bumping ships nothing
    # and `/plugin update` reports "already at the latest version". Falling through
    # to the SHA means every commit here is an update, which is what we want while
    # the tool surface is moving. Warn rather than fail, so pinning a release later
    # is a one-line change and not a fight with this script.
    if manifest.get("version"):
        warn(
            f"plugin.json pins version {manifest['version']} — updates now require bumping it "
            "on every change customers should receive; delete the field to version by commit SHA"
        )

    mcp_path = ROOT / str(manifest.get("mcpServers", ".mcp.json")).removeprefix("./")
    servers = load_json(mcp_path).get("mcpServers", {})
    if list(servers) != ["orchard"]:
        fail(f"{mcp_path.name}: expected exactly one server named 'orchard', got {list(servers)}")
    for name, cfg in servers.items():
        url = cfg.get("url", "")
        if not url.startswith("https://"):
            fail(f"{mcp_path.name}: server '{name}' url must be https, got {url!r}")
        path = "/" + url.split("://", 1)[-1].split("/", 1)[-1] if "://" in url else ""
        if endpoint and path != endpoint:
            fail(f"{mcp_path.name}: server '{name}' points at {path!r}; the API serves {endpoint!r}")

    market = load_json(ROOT / ".claude-plugin" / "marketplace.json")
    listed = {p.get("name") for p in market.get("plugins", [])}
    if manifest.get("name") and manifest["name"] not in listed:
        fail(f"marketplace.json lists {sorted(listed)} — not '{manifest['name']}' from plugin.json")
    return manifest


def check_tool_refs(path: pathlib.Path, tools: set[str]) -> set[str]:
    """Tools this file names. Anything shaped like a tool but unknown is drift."""
    text = path.read_text()
    where = path.relative_to(ROOT)
    named = set()
    for ref in sorted(set(TOOL_REF.findall(text))):
        if ref in tools:
            named.add(ref)
        else:
            fail(f"{where}: names tool '{ref}', which the server doesn't expose")
    for token in sorted(set(BACKTICKED.findall(text))):
        if token in tools:
            named.add(token)
        elif near := difflib.get_close_matches(token, sorted(tools), n=1, cutoff=0.85):
            fail(f"{where}: `{token}` looks like a stale tool name — did you mean `{near[0]}`?")
    return named


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tools", help="comma-separated tool names the MCP server exposes")
    ap.add_argument("--endpoint", help="the path the API serves the MCP server on, e.g. /v1/mcp")
    args = ap.parse_args()

    manifest = check_manifests(args.endpoint)
    readme = (ROOT / "README.md").read_text()
    tools = documented_tools(readme)

    if args.tools:
        served = {t.strip() for t in args.tools.split(",") if t.strip()}
        # Claiming a tool that doesn't exist is a lie to a customer — hard fail. The
        # reverse isn't: the MCP server is a general estate surface and the README is a
        # curated pitch, so "the server grew a tool" must never wedge a control-plane
        # deploy. Warn, and let a human decide whether it's worth advertising.
        if phantom := sorted(tools - served):
            fail(f"README.md: documents {', '.join(phantom)} — the server exposes no such tool")
        if undocumented := sorted(served - tools):
            warn(f"{len(undocumented)} server tool(s) not documented in README.md: {', '.join(undocumented)}")
        tools |= served

    commands = sorted((ROOT / "commands").glob("*.md"))
    if not commands:
        fail("commands/: no slash commands found")
    for cmd in commands:
        if not frontmatter(cmd).get("description"):
            fail(f"{cmd.relative_to(ROOT)}: frontmatter needs a 'description'")
        if not check_tool_refs(cmd, tools):
            fail(f"{cmd.relative_to(ROOT)}: names no Orchard tool — is it still wired to the server?")

    skills = sorted((ROOT / "skills").glob("*/SKILL.md"))
    for skill in skills:
        meta = frontmatter(skill)
        if meta.get("name") != skill.parent.name:
            fail(f"{skill.relative_to(ROOT)}: name '{meta.get('name')}' != directory '{skill.parent.name}'")
        if not meta.get("description"):
            fail(f"{skill.relative_to(ROOT)}: frontmatter needs a 'description'")
        check_tool_refs(skill, tools)

    for note in warnings:
        print(f"warning: {note}")
    if failures:
        print(f"{manifest.get('name', 'plugin')}: {len(failures)} problem(s)")
        for problem in failures:
            print(f"  - {problem}")
        return 1
    scope = "against the live server" if args.tools else "structure + README"
    version = f"v{manifest['version']}" if manifest.get("version") else "@commit-sha"
    print(f"{manifest.get('name')} {version}: ok ({scope}) — "
          f"{len(commands)} commands, {len(skills)} skills, {len(tools)} tools")
    return 0


if __name__ == "__main__":
    sys.exit(main())
