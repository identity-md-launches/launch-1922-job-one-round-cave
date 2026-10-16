import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from scout import InputError, parse_candidates, render_text, scout

DEMO = Path('line-2/tools/csv-key-scout')


class KeyScoutTests(unittest.TestCase):
    def test_demo_ranks_unique_candidate_and_reports_pairing_counts(self):
        candidates = [['record_id'], ['source_code'], ['area', 'record_id']]
        result = scout(DEMO / 'demo-before.csv', DEMO / 'demo-after.csv', candidates)
        by_columns = {tuple(item['columns']): item for item in result['candidates']}
        self.assertEqual(result['candidates'][0]['columns'], ['record_id'])
        self.assertEqual(by_columns[('record_id',)]['status'], 'review')
        self.assertEqual(by_columns[('record_id',)]['left']['eligible_unique_keys'], 4)
        self.assertEqual(by_columns[('record_id',)]['right']['empty_key_records'], 1)
        self.assertEqual(by_columns[('source_code',)]['left']['duplicate_groups'], 1)
        self.assertEqual(by_columns[('area', 'record_id')]['shared_eligible_keys'], 2)

    def test_missing_header_is_reported_without_cell_values(self):
        result = scout(DEMO / 'demo-before.csv', DEMO / 'demo-after.csv', [['label'], ['absent']])
        missing = next(item for item in result['candidates'] if item['columns'] == ['absent'])
        self.assertEqual(missing['left']['missing_columns'], ['absent'])
        self.assertIsNone(missing['shared_eligible_keys'])
        self.assertNotIn('sensitive-cell-sentinel', json.dumps(result))

    def test_candidate_specs_are_bounded_and_unambiguous(self):
        self.assertEqual(parse_candidates(['["id"]', '["code","region"]']), [['id'], ['code', 'region']])
        for specs in (['bad'], ['[]'], ['["id","id"]'], ['["id"]', '["id"]']):
            with self.subTest(specs=specs), self.assertRaises(InputError):
                parse_candidates(specs)

    def test_later_input_failure_does_not_return_partial_result(self):
        with self.assertRaises(OSError):
            scout(DEMO / 'demo-before.csv', Path('test/scratch/no-such-key-scout.csv'), [['record_id']])

    def test_text_has_counts_and_semantic_caveat(self):
        text = render_text(scout(DEMO / 'demo-before.csv', DEMO / 'demo-after.csv', [['record_id']]))
        self.assertIn('empty-key records', text)
        self.assertIn('does not choose a key', text)


if __name__ == '__main__':
    unittest.main()
