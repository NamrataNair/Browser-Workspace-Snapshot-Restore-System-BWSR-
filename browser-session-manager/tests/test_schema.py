import unittest
from models.schema import TabSession, WindowSession, BrowserSession, SessionSnapshot

class TestSchema(unittest.TestCase):
    def test_tab_session(self):
        tab = TabSession(url="https://example.com", title="Example", position=0)
        self.assertEqual(tab.url, "https://example.com")
        self.assertEqual(tab.title, "Example")

        data = tab.to_dict()
        self.assertEqual(data["url"], "https://example.com")

        tab_parsed = TabSession.from_dict(data)
        self.assertEqual(tab_parsed.url, tab.url)
        self.assertEqual(tab_parsed.position, tab.position)

    def test_window_session(self):
        tab1 = TabSession(url="https://a.com", position=0)
        tab2 = TabSession(url="https://b.com", position=1)
        win = WindowSession(incognito=True, tabs=[tab1, tab2])

        self.assertTrue(win.incognito)
        self.assertEqual(len(win.tabs), 2)

        data = win.to_dict()
        self.assertTrue(data["incognito"])
        self.assertEqual(len(data["tabs"]), 2)

        win_parsed = WindowSession.from_dict(data)
        self.assertTrue(win_parsed.incognito)
        self.assertEqual(win_parsed.tabs[0].url, "https://a.com")

    def test_browser_session(self):
        win = WindowSession(incognito=False, tabs=[TabSession(url="https://c.com")])
        browser = BrowserSession(browser="chrome", browser_version="1.0", windows=[win])

        data = browser.to_dict()
        self.assertEqual(data["browser"], "chrome")

        browser_parsed = BrowserSession.from_dict(data)
        self.assertEqual(browser_parsed.browser, "chrome")
        self.assertEqual(len(browser_parsed.windows), 1)

    def test_session_snapshot(self):
        browser = BrowserSession(browser="firefox", windows=[])
        snapshot = SessionSnapshot(machine="TEST-MACHINE", timestamp="2024-01-01T12:00:00", browsers=[browser])

        data = snapshot.to_dict()
        self.assertEqual(data["machine"], "TEST-MACHINE")
        self.assertEqual(len(data["browsers"]), 1)

        snapshot_parsed = SessionSnapshot.from_dict(data)
        self.assertEqual(snapshot_parsed.machine, "TEST-MACHINE")
        self.assertEqual(snapshot_parsed.browsers[0].browser, "firefox")

if __name__ == "__main__":
    unittest.main()
