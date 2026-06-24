import unittest
from unittest.mock import patch
from restorer.restore import SessionRestorer

class TestRestorer(unittest.TestCase):
    @patch('sys.platform', 'linux')
    @patch('builtins.open', create=True)
    def test_get_browser_executable_linux_native(self, mock_open):
        mock_open.side_effect = FileNotFoundError() # not wsl

        restorer = SessionRestorer("dummy.json")
        self.assertEqual(restorer.get_browser_executable("chrome"), "google-chrome")
        self.assertEqual(restorer.get_browser_executable("edge"), "microsoft-edge")

    @patch('sys.platform', 'win32')
    def test_get_browser_executable_win(self):
        restorer = SessionRestorer("dummy.json")
        self.assertEqual(restorer.get_browser_executable("chrome"), "chrome.exe")
        self.assertEqual(restorer.get_browser_executable("firefox"), "firefox.exe")

if __name__ == "__main__":
    unittest.main()
