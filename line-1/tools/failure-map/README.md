# Failure Map

Failure Map classifies one saved, bounded public HTTP probe by the phase where
it observed trouble: DNS, connection, TLS, timeout, response headers/body,
JSON, or an HTTP/check failure. It performs no network request, retry, wait,
wallet action, or clock read, and uses only Python's standard library.

Run the real retained observation offline:

```sh
python3 -B line-1/tools/failure-map/failure_map.py line-1/tools/endpoint-sentry/live-failure.json
```

Expected result is a nonzero exit and JSON identifying the recorded failure
phase. A successful capture exits 0. This is a diagnosis of one observation,
not a root-cause guarantee or a statement about current availability.

What happened when tried: the retained anonymous public failure classified as
an HTTP-status failure, while the retained successful capture classified as a
healthy observation. Tests cover watchdog failures, transport errors, HTTP
statuses, failed checks, malformed input, and workspace confinement.
