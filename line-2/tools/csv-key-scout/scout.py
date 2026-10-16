#!/usr/bin/env python3
"""Rank explicit CSV key candidates by exact, value-free data-quality counts."""
import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'csv-reconcile'))
from reconcile import InputError, load_table

MAX_CANDIDATES = 20
MAX_COLUMNS_PER_CANDIDATE = 4


def parse_candidates(specifications):
    """Parse repeatable JSON arrays such as '["id"]' and '["code","region"]'."""
    if not 1 <= len(specifications) <= MAX_CANDIDATES:
        raise InputError(f'provide 1 to {MAX_CANDIDATES} candidates')
    candidates = []
    seen = set()
    for index, specification in enumerate(specifications, 1):
        try:
            columns = json.loads(specification)
        except json.JSONDecodeError as exc:
            raise InputError(f'candidate {index} must be a JSON array of column names') from exc
        if (not isinstance(columns, list) or not 1 <= len(columns) <= MAX_COLUMNS_PER_CANDIDATE
                or any(not isinstance(column, str) or not column for column in columns)):
            raise InputError(f'candidate {index} needs 1 to {MAX_COLUMNS_PER_CANDIDATE} nonempty column names')
        if len(set(columns)) != len(columns):
            raise InputError(f'candidate {index} repeats a column')
        identity = frozenset(columns)
        if identity in seen:
            raise InputError(f'candidate {index} repeats an earlier column set')
        seen.add(identity)
        candidates.append(columns)
    return candidates


def _rows(groups):
    # load_table(..., []) retains source order in the single empty-tuple bucket.
    return [item['values'] for item in groups.get((), [])]


def _side_summary(header, rows, columns):
    missing = [column for column in columns if column not in header]
    result = {'records': len(rows), 'missing_columns': missing}
    if missing:
        return result, None
    groups = {}
    empty_records = 0
    for row in rows:
        key = tuple(row[column] for column in columns)
        if any(value == '' for value in key):
            empty_records += 1
            continue
        groups[key] = groups.get(key, 0) + 1
    duplicate_counts = [count for count in groups.values() if count > 1]
    eligible = {key for key, count in groups.items() if count == 1}
    result.update({
        'empty_key_records': empty_records,
        'duplicate_groups': len(duplicate_counts),
        'duplicate_records': sum(duplicate_counts),
        'eligible_unique_keys': len(eligible),
    })
    return result, eligible


def scout(before, after, candidates):
    """Compare explicitly supplied candidate columns; no cell values are returned."""
    if not 1 <= len(candidates) <= MAX_CANDIDATES:
        raise InputError(f'provide 1 to {MAX_CANDIDATES} candidates')
    for index, columns in enumerate(candidates, 1):
        if (not isinstance(columns, list) or not 1 <= len(columns) <= MAX_COLUMNS_PER_CANDIDATE
                or any(not isinstance(column, str) or not column for column in columns)
                or len(set(columns)) != len(columns)):
            raise InputError(f'candidate {index} needs distinct, nonempty column names')

    before_header, before_groups, _ = load_table(before, [])
    after_header, after_groups, _ = load_table(after, [])
    before_rows, after_rows = _rows(before_groups), _rows(after_groups)
    results = []
    for index, columns in enumerate(candidates, 1):
        left, left_keys = _side_summary(before_header, before_rows, columns)
        right, right_keys = _side_summary(after_header, after_rows, columns)
        missing = bool(left['missing_columns'] or right['missing_columns'])
        if missing:
            shared = left_only = right_only = None
            ready = False
        else:
            shared = len(left_keys & right_keys)
            left_only = len(left_keys - right_keys)
            right_only = len(right_keys - left_keys)
            ready = bool(left['records'] and right['records']) and all(
                side['empty_key_records'] == 0 and side['duplicate_groups'] == 0
                for side in (left, right))
        results.append({
            'candidate_index': index,
            'columns': columns,
            'status': 'ready_in_these_files' if ready else 'review',
            'left': left,
            'right': right,
            'shared_eligible_keys': shared,
            'left_only_eligible_keys': left_only,
            'right_only_eligible_keys': right_only,
        })

    results.sort(key=lambda item: (
        item['status'] != 'ready_in_these_files',
        -(item['shared_eligible_keys'] or 0),
        -((item['left'].get('eligible_unique_keys') or 0)
          + (item['right'].get('eligible_unique_keys') or 0)),
        len(item['columns']),
        tuple(item['columns']),
    ))
    for rank, item in enumerate(results, 1):
        item['rank'] = rank
    return {
        'format': 'csv-key-scout/v1',
        'candidates': results,
        'ordering': ('ready candidates first, then shared eligible keys, then total eligible keys, '
                     'then fewer columns; remaining ties by column names'),
        'caution': ('Ranking describes these two files only. It does not choose a key or prove that any column '
                    'identifies the same real-world record across exports.'),
    }


def render_text(result):
    lines = [f"CSV key candidate scout: {len(result['candidates'])} candidates"]
    for item in result['candidates']:
        lines.append(f"Rank {item['rank']}: {json.dumps(item['columns'], ensure_ascii=False)} — {item['status']}")
        for label in ('left', 'right'):
            side = item[label]
            if side['missing_columns']:
                lines.append(f"  {label}: {side['records']} records; missing columns: "
                             f"{json.dumps(side['missing_columns'], ensure_ascii=False)}")
            else:
                lines.append(f"  {label}: {side['records']} records; "
                             f"{side['eligible_unique_keys']} eligible unique keys; "
                             f"{side['empty_key_records']} empty-key records; "
                             f"{side['duplicate_groups']} duplicate groups.")
        if item['shared_eligible_keys'] is not None:
            lines.append(f"  shared eligible keys: {item['shared_eligible_keys']}; "
                         f"left only: {item['left_only_eligible_keys']}; "
                         f"right only: {item['right_only_eligible_keys']}.")
    lines.append(result['caution'])
    return '\n'.join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('before', help='baseline CSV inside the current working directory')
    parser.add_argument('after', help='candidate CSV inside the current working directory')
    parser.add_argument('--candidate', action='append', required=True, metavar='JSON',
                        help='JSON array of 1–4 column names; repeat to compare candidates')
    parser.add_argument('--format', choices=('text', 'json'), default='text')
    args = parser.parse_args(argv)
    try:
        candidates = parse_candidates(args.candidate)
        result = scout(args.before, args.after, candidates)
        output = render_text(result) if args.format == 'text' else json.dumps(
            result, ensure_ascii=False, sort_keys=True, indent=2)
    except (InputError, OSError, ValueError) as exc:
        print(json.dumps({'error': str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(output)
    return 0


if __name__ == '__main__':
    sys.exit(main())
