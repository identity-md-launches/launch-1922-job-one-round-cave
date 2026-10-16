#!/usr/bin/env python3
"""Inspect explicit CSV key candidates, then summarize only a human-selected key."""
import argparse
import json
import sys

import change_summary
import key_candidates

NOTICE = ('Candidate statistics describe these files only, not semantic identity. '
          'No key is selected automatically. Headers, schema and counts are exposed; '
          'data-cell values are omitted. Inputs must remain stable across reads. '
          'Equal evidence does not establish source health, recency or chain state.')


def review(before, after, candidates, selected=None):
    # Use the same validation for API and CLI callers, including duplicate sets.
    candidates = key_candidates.parse_candidates([json.dumps(c) for c in candidates])
    if selected is not None:
        if (not isinstance(selected, list) or not selected
                or any(not isinstance(c, str) or not c for c in selected)
                or len(set(selected)) != len(selected)
                or not any(set(selected) == set(c) for c in candidates)):
            raise ValueError('selected key must be one of the explicit candidate sets')
    scout = key_candidates.scout(before, after, candidates)
    result = {'format': 'csv-candidate-review/v1', 'scope': NOTICE,
              'candidates': scout['candidates'], 'selected_key': selected,
              'state': 'awaiting_selection', 'comparison': None,
              'cell_values_included': False}
    if selected is None:
        return result
    chosen = next(c for c in scout['candidates'] if set(c['columns']) == set(selected))
    if chosen['status'] != 'ready_in_these_files':
        result['state'] = 'blocked_key_quality'
        return result
    comparison = change_summary.summarize(before, after, selected)
    # Re-check selected-key quality after the summary's reads. This is not a
    # filesystem lock: callers must keep both inputs unchanged throughout.
    for path in (before, after):
        _, groups, count = key_candidates.load_table(path, selected)
        if not count or any('' in key or len(rows) != 1 for key, rows in groups.items()):
            raise ValueError('key quality changed during review')
    result.update(state='compared', comparison=comparison)
    return result


def exit_code(result):
    if result['state'] == 'awaiting_selection':
        return 0
    return int(result['state'] != 'compared' or not result['comparison']['equal'])


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument('before')
    parser.add_argument('after')
    parser.add_argument('--candidate', action='append', required=True, metavar='JSON')
    parser.add_argument('--key', action='append', help='explicit chosen column; repeat for a composite key')
    args = parser.parse_args(argv)
    try:
        candidates = key_candidates.parse_candidates(args.candidate)
        result = review(args.before, args.after, candidates, args.key)
    except (ValueError, OSError, TypeError, RecursionError):
        print(json.dumps({'error': 'Invalid workspace CSVs, candidates or selected key.'}), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return exit_code(result)


if __name__ == '__main__':
    sys.exit(main())
