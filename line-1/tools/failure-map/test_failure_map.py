import json
import tempfile
import unittest
from pathlib import Path
import importlib.util

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("failure_map", HERE / "failure_map.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

class FailureMapTests(unittest.TestCase):
    def test_transport(self):
        r = m.classify({"schema":"endpoint-sentry/v1", "ok":False,
                        "error":{"kind":"tls", "message":"bad cert"}})
        self.assertEqual((r["outcome"], r["phase"]), ("failure-observed", "TLS handshake"))
    def test_http_status(self):
        r = m.classify({"schema":"endpoint-sentry/v1", "ok":False,
                        "hops":[{"status":503}], "checks":[{"name":"status","ok":False}]})
        self.assertEqual(r["status"], 503)
    def test_success(self):
        self.assertEqual(m.classify({"schema":"endpoint-sentry/v1", "ok":True})["outcome"], "healthy-observation")
    def test_wrapper_without_worker(self):
        self.assertEqual(m.classify({"schema":"deadline-sentry/v1"})["phase"], "unknown")
    def test_bad_file(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/"x.json"; p.write_text("{}")
            with self.assertRaises(ValueError): m.load(str(p))

if __name__ == "__main__": unittest.main()
