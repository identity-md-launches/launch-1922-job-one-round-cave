"""Cross-line key choice must remain explicit and keep cell values out of review."""
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest

import candidate_review as tool

TOKENS = 'shared/token-read-plan/observed.csv'
TOKEN_KEY = ['chain_id', 'token_address', 'field']


class CandidateReviewTests(unittest.TestCase):
    def setUp(self):
        Path('test/scratch').mkdir(parents=True, exist_ok=True)
        temp = tempfile.TemporaryDirectory(dir='test/scratch')
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)

    def save(self, name, text):
        p = self.root / name
        p.write_text(text)
        return p

    def test_real_retained_tokens_do_not_automatically_choose_top_rank(self):
        r = tool.review(TOKENS, TOKENS, [['token_address'], TOKEN_KEY])
        self.assertEqual(r['state'], 'awaiting_selection')
        self.assertIsNone(r['comparison'])
        self.assertIsNone(r['selected_key'])
        self.assertEqual(r['candidates'][0]['columns'], TOKEN_KEY)
        self.assertEqual(r['candidates'][0]['shared_eligible_keys'], 6)
        self.assertEqual(tool.exit_code(r), 0)

    def test_real_tokens_explicit_composite_key_compares_without_values(self):
        r = tool.review(TOKENS, TOKENS, [['token_address'], TOKEN_KEY], TOKEN_KEY)
        self.assertTrue(r['comparison']['equal'])
        self.assertEqual(r['comparison']['summary']['before_records'], 6)
        self.assertNotIn('0xd782', json.dumps(r))
        self.assertEqual(tool.exit_code(r), 0)

    def test_duplicate_token_key_blocks_even_when_another_candidate_is_ready(self):
        r = tool.review(TOKENS, TOKENS, [TOKEN_KEY, ['token_address']], ['token_address'])
        self.assertEqual(r['state'], 'blocked_key_quality')
        self.assertIsNone(r['comparison'])
        self.assertEqual(tool.exit_code(r), 1)

    def test_age_handoff_reports_exact_changed_columns(self):
        r = tool.review('shared/http-evidence/observed-age-recent34.csv',
                        'shared/http-evidence/observed-age-stale34.csv', [['url']], ['url'])
        self.assertEqual({x['column'] for x in r['comparison']['changed_columns']},
                         {'outcome', 'age_seconds', 'evaluated_at'})
        self.assertNotIn('https://api.imd.fun', json.dumps(r))
        self.assertEqual(tool.exit_code(r), 1)

    def test_empty_missing_and_duplicate_keys_are_not_applied(self):
        for text, key in [('id,value\n,private\n', 'id'),
                          ('id,value\na,private\na,other\n', 'id'),
                          ('id,value\n', 'id'), ('id,value\na,private\n', 'missing')]:
            p = self.save('rows.csv', text)
            r = tool.review(p, p, [[key]], [key])
            self.assertEqual(r['state'], 'blocked_key_quality')
            self.assertIsNone(r['comparison'])
            self.assertNotIn('private', json.dumps(r))

    def test_unlisted_key_and_duplicate_candidate_sets_refuse(self):
        for candidates, selected in [([TOKEN_KEY], ['field']),
                                     ([TOKEN_KEY, TOKEN_KEY[::-1]], None),
                                     ([TOKEN_KEY], ['field', 'field'])]:
            with self.assertRaises(ValueError):
                tool.review(TOKENS, TOKENS, candidates, selected)

    def test_error_does_not_expose_filename_or_csv_cells(self):
        p = self.save('private-name.csv', 'id,id\nprivate,other\n')
        with contextlib.redirect_stdout(io.StringIO()) as out, contextlib.redirect_stderr(io.StringIO()) as err:
            code = tool.main([str(p), str(p), '--candidate', '["id"]', '--key', 'id'])
        self.assertEqual(code, 2)
        self.assertEqual(out.getvalue(), '')
        self.assertNotIn('private', err.getvalue())

    def test_changed_schema_stays_unequal_with_no_changed_cells(self):
        a = self.save('a.csv', 'id,value\na,one\n')
        b = self.save('b.csv', 'id,value,extra\na,one,two\n')
        r = tool.review(a, b, [['id']], ['id'])
        self.assertFalse(r['comparison']['equal'])
        self.assertEqual(r['comparison']['changed_cells_on_common_columns'], 0)
        self.assertEqual(r['comparison']['schema']['added_columns'], ['extra'])


if __name__ == '__main__':
    unittest.main()
