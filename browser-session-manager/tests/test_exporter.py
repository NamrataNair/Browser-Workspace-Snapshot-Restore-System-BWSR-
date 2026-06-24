import unittest
from exporter.session_exporter import SessionExporter
from models.schema import BrowserSession
import os

class TestExporter(unittest.TestCase):
    def test_export(self):
        output_path = "test_session_export.json"
        exporter = SessionExporter(output_path)

        session = BrowserSession(browser="dummy")
        snapshot = exporter.export([session])

        self.assertTrue(os.path.exists(output_path))
        self.assertEqual(snapshot.browsers[0].browser, "dummy")

        os.remove(output_path)

if __name__ == "__main__":
    unittest.main()
