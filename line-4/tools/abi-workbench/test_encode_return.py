"""CLI checks for canonical offline return-byte construction."""
import contextlib
import io
import json
from pathlib import Path
import unittest
from unittest.mock import patch

import abi_workbench as abi


ABI = Path(__file__).with_name('tuple-example.json')


def run(*arguments):
    stdout, stderr = io.StringIO(), io.StringIO()
    with patch('sys.argv', ['abi_workbench', *arguments]), \
         contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        code = abi.main()
    return code, stdout.getvalue(), stderr.getvalue()


class EncodeReturnTests(unittest.TestCase):
    def test_dynamic_tuple_layout_and_strict_round_trip(self):
        code, output, error = run('encode-return', '--abi', str(ABI),
                                  '--function', 'get(uint256)', '--values', '[[7,"ZTO"]]')
        self.assertEqual((code, error), (0, ''))
        payload = json.loads(output)
        self.assertEqual(payload['signature'], 'get(uint256)')
        # Independent ABI layout: outer offset, tuple uint, inner string offset,
        # string byte count, then the padded three-byte string.
        expected = (abi.word(32) + abi.word(7) + abi.word(64) +
                    abi.word(3) + b'ZTO'.ljust(32, b'\0'))
        self.assertEqual(payload['return_data'], '0x' + expected.hex())
        code, output, error = run('decode', '--abi', str(ABI), '--function', 'get',
                                  '--strict', '--data', payload['return_data'])
        self.assertEqual((code, error), (0, ''))
        self.assertEqual(json.loads(output)['outputs'][0]['value'], [7, 'ZTO'])

    def test_no_outputs_is_empty_bytes(self):
        code, output, error = run('encode-return', '--abi', str(ABI),
                                  '--function', 'put', '--values', '[]')
        self.assertEqual((code, error), (0, ''))
        self.assertEqual(json.loads(output)['return_data'], '0x')

    def test_wrong_shape_and_count_refuse_without_success_output(self):
        for values in ('7', '[]', '[[7]]', '[[7,"ZTO"],8]'):
            with self.subTest(values=values):
                code, output, error = run('encode-return', '--abi', str(ABI),
                                          '--function', 'get', '--values', values)
                self.assertEqual(code, 2)
                self.assertEqual(output, '')
                self.assertTrue(error.startswith('error: '))


if __name__ == '__main__':
    unittest.main()
