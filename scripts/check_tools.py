#!/usr/bin/env python
"""The lab bench check: every tool the AI-200 labs use, its version, green or red.

    python scripts/check_tools.py

Exit code 0 when every tool is present (and new enough), 1 when a required one is missing.
Works anywhere: a missing tool is just a red line.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass

GREEN, RED, RESET = "\033[32m", "\033[31m", "\033[0m"


@dataclass
class Tool:
    name: str
    command: list[str]  # prints the version
    minimum: tuple[int, ...] | None = None
    why: str = ""


def parse_version(text: str) -> tuple[int, ...] | None:
    m = re.search(r"(\d+)\.(\d+)(?:\.(\d+))?", text)
    return tuple(int(g) for g in m.groups() if g is not None) if m else None


def run(command: list[str], timeout: int = 45) -> str | None:
    """Output of the command, or None when it is missing or fails."""
    if shutil.which(command[0]) is None:
        return None
    try:
        done = subprocess.run(command, capture_output=True, text=True, timeout=timeout, check=False)
    except (OSError, subprocess.TimeoutExpired):
        return None
    return (done.stdout + done.stderr).strip() if done.returncode == 0 else None


def az_info() -> dict:
    out = run(["az", "version", "--output", "json"])
    try:
        return json.loads(out) if out else {}
    except ValueError:
        return {}


TOOLS = [
    Tool("Python", [sys.executable, "--version"], (3, 12), "every lab"),
    Tool("Git", ["git", "--version"], None, "clone and commit"),
    Tool("Azure CLI", ["az", "version", "--output", "json"], (2, 80), "az commands; 2.80+ for Foundry projects"),
    Tool("Bicep", ["bicep", "--version"], None, "infrastructure files"),
    Tool("Docker", ["docker", "--version"], None, "build and run images"),
    Tool("Functions Core Tools", ["func", "--version"], (4,), "run Azure Functions locally"),
    Tool("Azurite", ["azurite", "--version"], None, "local storage for Functions triggers"),
    Tool("kubectl", ["kubectl", "version", "--client"], None, "the AKS labs"),
    Tool("psql", ["psql", "--version"], None, "the PostgreSQL labs"),
]
EXTENSIONS = [
    ("containerapp", "az extension: containerapp"),
    ("redisenterprise", "az extension: redisenterprise"),
]


def check_tool(tool: Tool, info: dict) -> tuple[bool, str]:
    if tool.name == "Python":
        out = sys.version.split()[0]
    elif tool.name == "Azure CLI":
        out = info.get("azure-cli", "") if info else ""
    elif tool.name == "Bicep":
        out = run(["bicep", "--version"]) or run(["az", "bicep", "version"]) or ""
    else:
        out = run(tool.command) or ""
    version = parse_version(out)
    if not out or version is None:
        return False, "not found"
    if tool.minimum and version[: len(tool.minimum)] < tool.minimum:
        need = ".".join(map(str, tool.minimum))
        return False, f"{'.'.join(map(str, version))} (need {need} or newer)"
    return True, ".".join(map(str, version))


def main() -> int:
    color = sys.stdout.isatty() and "NO_COLOR" not in os.environ
    g, r, z = (GREEN, RED, RESET) if color else ("", "", "")
    info = az_info()
    rows: list[tuple[bool, str, str, str]] = []
    for tool in TOOLS:
        ok, detail = check_tool(tool, info)
        rows.append((ok, tool.name, detail, tool.why))
    installed = (info or {}).get("extensions", {})
    for ext, label in EXTENSIONS:
        have = installed.get(ext)
        rows.append((bool(have), label, have or f"not installed (az extension add --name {ext})", ""))
    width = max(len(name) for _, name, _, _ in rows)
    print("CornerCart lab bench")
    for ok, name, detail, why in rows:
        mark = f"{g}OK     {z}" if ok else f"{r}MISSING{z}"
        print(f"  {mark} {name:<{width}}  {detail}" + (f"   ({why})" if why and not ok else ""))
    missing = [name for ok, name, _, _ in rows if not ok]
    print()
    if missing:
        print(f"{r}{len(missing)} missing: {', '.join(missing)}{z}")
        return 1
    print(f"{g}All {len(rows)} tools are ready.{z}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
