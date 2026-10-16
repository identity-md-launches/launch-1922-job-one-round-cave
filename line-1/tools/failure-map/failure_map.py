#!/usr/bin/env python3
"""Classify one saved Endpoint Sentry report by its observed failure phase."""
import argparse
import json
from pathlib import Path
import sys

SCHEMA = "failure-map/v1"
PHASES = {
    "dns": "name resolution",
    "tls": "TLS handshake",
    "connect": "TCP connection",
    "timeout": "deadline or read timeout",
    "headers": "HTTP response headers",
    "body": "HTTP response body",
    "json": "JSON validation",
    "json_pointer": "JSON expectation",
}

def load(path):
    p = Path(path).resolve()
    cwd = Path.cwd().resolve()
    if not p.is_relative_to(cwd) or not p.is_file() or p.stat().st_size > 1048576:
        raise ValueError("report must be a regular file inside the workspace, at most 1 MiB")
    with p.open("r", encoding="utf-8") as f:
        value = json.load(f)
    if not isinstance(value, dict):
        raise ValueError("report must be an object")
    if value.get("schema") == "deadline-sentry/v1":
        if "probe" not in value:
            return {"schema": SCHEMA, "outcome": "watchdog-failure",
                    "phase": "worker deadline", "evidence": "/error"}
        value = value["probe"]
    if value.get("schema") != "endpoint-sentry/v1":
        raise ValueError("expected Endpoint Sentry or Deadline Sentry report")
    return value

def classify(report):
    if report.get("ok") is True:
        return {"schema": SCHEMA, "outcome": "healthy-observation",
                "phase": "completed checks", "evidence": "/checks",
                "reason": "The captured probe passed its requested checks."}
    error = report.get("error")
    if isinstance(error, dict) and isinstance(error.get("kind"), str):
        kind = error["kind"]
        phase = PHASES.get(kind, kind)
        return {"schema": SCHEMA, "outcome": "failure-observed", "phase": phase,
                "evidence": "/error/kind", "reason": error.get("message", "recorded error")}
    hops = report.get("hops")
    if isinstance(hops, list) and hops and isinstance(hops[-1], dict):
        hop = hops[-1]
        status = hop.get("status")
        if isinstance(status, int):
            return {"schema": SCHEMA, "outcome": "http-failure", "phase": "HTTP status",
                    "status": status, "evidence": "/hops/{}/status".format(len(hops)-1),
                    "reason": "The server returned a status that did not satisfy the request."}
    checks = report.get("checks")
    if isinstance(checks, list):
        failed = next((c for c in checks if isinstance(c, dict) and c.get("ok") is False), None)
        if failed:
            return {"schema": SCHEMA, "outcome": "check-failure", "phase": str(failed.get("name", "check")),
                    "evidence": "/checks/{}".format(checks.index(failed)),
                    "reason": "A requested check failed after a response was captured."}
    return {"schema": SCHEMA, "outcome": "insufficient-evidence", "phase": "unknown",
            "evidence": "/", "reason": "The report has no usable phase evidence."}

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    ap.add_argument("report")
    args = ap.parse_args(argv)
    try:
        result = classify(load(args.report))
    except (OSError, ValueError, UnicodeError, json.JSONDecodeError, RecursionError):
        print(json.dumps({"schema": SCHEMA, "error": "Invalid report or workspace path."}))
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["outcome"] == "healthy-observation" else 1

if __name__ == "__main__":
    sys.exit(main())
