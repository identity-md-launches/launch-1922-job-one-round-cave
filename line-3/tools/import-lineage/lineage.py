#!/usr/bin/env python3
"""Print a shortest, source-only import lineage between two local modules."""
from __future__ import annotations

import ast
import json
import pathlib
import sys
from collections import deque


def modules(root: pathlib.Path) -> dict[str, pathlib.Path]:
    result = {}
    for path in root.rglob("*.py"):
        rel = path.relative_to(root).with_suffix("")
        parts = list(rel.parts)
        if parts[-1] == "__init__":
            parts.pop()
        result[".".join(parts)] = path
    return result


def imports(path: pathlib.Path, name: str, known: set[str]) -> set[str]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (OSError, SyntaxError, UnicodeError):
        return set()
    package = name.split(".")[:-1]
    found = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            found.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            base = package[: max(0, len(package) - node.level + 1)]
            if node.level == 0:
                base = []
            prefix = ".".join(base + ([node.module] if node.module else []))
            for alias in node.names:
                candidate = prefix if alias.name == "*" else ".".join(x for x in (prefix, alias.name) if x)
                found.add(candidate)
    return {candidate for candidate in known if candidate == name or candidate.startswith(candidate + ".") or candidate in found}


def lineage(root: pathlib.Path, start: str, target: str) -> list[str] | None:
    known = modules(root)
    if start not in known or target not in known:
        return None
    queue = deque([(start, [start])])
    seen = {start}
    while queue:
        current, path = queue.popleft()
        if current == target:
            return path
        for nxt in sorted(imports(known[current], current, set(known))):
            if nxt not in seen:
                seen.add(nxt)
                queue.append((nxt, path + [nxt]))
    return None


if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise SystemExit("usage: lineage.py ROOT START_MODULE TARGET_MODULE")
    answer = lineage(pathlib.Path(sys.argv[1]), sys.argv[2], sys.argv[3])
    print(json.dumps({"found": answer is not None, "path": answer}, indent=2))
