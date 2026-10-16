#!/usr/bin/env python3
"""Current CLI trials and explicit reproductions; no writes to line folders."""
import json
from pathlib import Path
import subprocess
import sys


def main():
    scratch = Path('test/scratch/gathering35/current')
    scratch.mkdir(parents=True, exist_ok=True)
    results = []

    def run(label, script, args, expected=0, save=None):
        command = [sys.executable, '-B', script, *map(str, args)]
        p = subprocess.run(command, capture_output=True, text=True, timeout=25)
        try:
            value = json.loads(p.stdout)
        except ValueError:
            value = p.stdout
        results.append(dict(name=label, command=command, exit_code=p.returncode,
                            expected_exit_code=expected, passed=p.returncode == expected,
                            output=value, stderr=p.stderr[:1500]))
        if save:
            Path(save).write_text(p.stdout)
        return value

    run('Failure Map retained public HTTP failure', 'line-1/tools/failure-map/failure_map.py',
        ['line-1/tools/endpoint-sentry/live-failure.json'], 1)
    run('Failure Map retained successful capture', 'line-1/tools/failure-map/failure_map.py',
        ['line-1/tools/endpoint-sentry/live-success.json'])
    watchdog = scratch/'watchdog.json'
    watchdog.write_text(json.dumps(dict(schema='deadline-sentry/v1', ok=False,
                                      error=dict(kind='deadline', message='worker killed'))))
    r = run('Reproduced bug: Failure Map drops explicit watchdog phase',
            'line-1/tools/failure-map/failure_map.py', [watchdog], 1)
    assert r['outcome'] == 'insufficient-evidence' and r['phase'] == 'unknown'
    checked = scratch/'check.json'
    checked.write_text(json.dumps(dict(schema='endpoint-sentry/v1', ok=False,
                         hops=[dict(status=200)], checks=[dict(name='status', ok=True),
                                                        dict(name='json_value', ok=False)])))
    r = run('Reproduced bug: failed JSON value after HTTP 200 mislabeled HTTP failure',
            'line-1/tools/failure-map/failure_map.py', [checked], 1)
    assert r['outcome'] == 'http-failure' and r['status'] == 200
    run('Framing Lens real retained capture', 'line-1/tools/framing-lens/framing_lens.py',
        ['line-1/tools/framing-lens/observed-live.json'])
    run('Freshness Lens explicit historical time', 'line-1/tools/freshness-lens/freshness_lens.py',
        ['line-1/tools/endpoint-doctor/observed-live.json', '--at', '2026-10-15T23:03:23.567439Z', '--max-age', '300'])
    run('Key Scout documented demo', 'line-2/tools/csv-key-scout/scout.py',
        ['line-2/tools/csv-key-scout/demo-before.csv', 'line-2/tools/csv-key-scout/demo-after.csv',
         '--candidate', '["record_id"]', '--candidate', '["source_code"]',
         '--candidate', '["area","record_id"]', '--format', 'json'])
    run('CSV summary inventory', 'line-2/tools/csv-summary/summary.py',
        ['line-2/tools/csv-gate/demo-before.csv', 'line-2/tools/csv-gate/demo-after.csv', '--key', 'item'], 1)
    run('CSV slice empty window retains global unequal verdict', 'line-2/tools/csv-slice/slice.py',
        ['line-2/tools/csv-gate/demo-before.csv', 'line-2/tools/csv-gate/demo-after.csv', '--key', 'item', '--offset', '999'], 1)
    run('External imports actual shared worker', 'line-3/tools/import-externals/externals.py',
        ['shared/import-drift', '--json', '--strict'])
    run('Origin Trace alias and wildcard fixture', 'line-3/tools/import-origin-trace/origins.py',
        ['line-3/tools/import-origin-trace/examples', '--json', '--strict'], 1)
    run('Import Lineage documented fixture', 'line-3/tools/import-lineage/lineage.py',
        ['line-3/tools/import-lineage/examples', 'app', 'service'])
    root = scratch/'lineage'
    root.mkdir(exist_ok=True)
    (root/'app.py').write_text('from service import run\n')
    (root/'service.py').write_text('def run():\n    return 1\n')
    r = run('Reproduced bug: Import Lineage misses from-module symbol import',
            'line-3/tools/import-lineage/lineage.py', [root, 'app', 'service'])
    assert r == {'found': False, 'path': None}
    corrected = run('Existing Import Route sees same explicit local import',
                    'line-3/tools/import-route/route.py', [root, 'app', 'service', '--json'])
    assert corrected['reachable']
    run('Calldata Rehearsal unsigned real ZTO address argument',
        'line-4/tools/calldata-rehearsal/calldata_rehearsal.py',
        ['--selector', '0x70a08231', '--types', 'address', '--values',
         '0xd782bdea4ef02a0bd391eb9089470c8080f0a68e'])
    run('Event Lens explicit constructed offline fixture', 'line-4/tools/event-lens/event_lens.py', ['--demo'])

    common = ['shared/token-read-plan/observed.csv']*2 + [
        '--candidate', '["token_address"]', '--candidate', '["chain_id","token_address","field"]']
    tool = 'shared/http-evidence/candidate_review.py'
    run('Shared token candidate preflight makes no selection', tool, common,
        save='shared/http-evidence/observed-candidates35.json')
    run('Shared human-selected real token composite key compares equal', tool,
        common + ['--key', 'chain_id', '--key', 'token_address', '--key', 'field'])
    run('Shared ambiguous token-only key blocked', tool, common + ['--key', 'token_address'], 1)
    run('Shared HTTP age key yields three changed columns', tool,
        ['shared/http-evidence/observed-age-recent34.csv', 'shared/http-evidence/observed-age-stale34.csv',
         '--candidate', '["url"]', '--key', 'url'], 1,
        save='shared/http-evidence/observed-candidate-age35.json')

    # A few anonymous reads, no transaction RPCs, no retries or timer waits.
    live = 'gathering/live-http35.json'
    run('Live Deadline Sentry anonymous public GET', 'line-1/tools/deadline-sentry/deadline_sentry.py',
        ['--deadline', '8', 'https://api.imd.fun/launches', '--timeout', '5',
         '--max-bytes', '262144', '--max-redirects', '0', '--json'], save=live)
    run('Endpoint Sentry direct bounded GET', 'line-1/tools/endpoint-sentry/sentry.py',
        ['https://api.imd.fun/launches', '--timeout', '5', '--max-bytes', '262144', '--max-redirects', '0', '--json'])
    run('TLS Route verified public origin', 'line-1/tools/tls-route/tls_route.py',
        ['https://api.imd.fun', '--deadline', '8', '--per-address', '2', '--max-addresses', '2'])
    run('Burst Sentry two bounded public GETs', 'line-1/tools/burst-sentry/burst_sentry.py',
        ['https://api.imd.fun/launches', '--samples', '2', '--budget', '10', '--per-probe', '4',
         '--timeout', '3', '--max-bytes', '262144', '--max-redirects', '0', '--json'])
    run('Endpoint Doctor diagnoses fresh captured source offline', 'line-1/tools/endpoint-doctor/endpoint_doctor.py',
        ['--report', live, '--format', 'json', '--require-complete'])
    report = dict(round=35, ok=all(r['passed'] for r in results), results=results,
                  known_bugs_reproduced=3)
    Path('gathering/current-checks35.json').write_text(json.dumps(report, separators=(',', ':'))+'\n')
    print(json.dumps(dict(ok=report['ok'], checks=len(results),
                          failed=[r['name'] for r in results if not r['passed']])))
    return int(not report['ok'])


if __name__ == '__main__':
    raise SystemExit(main())
