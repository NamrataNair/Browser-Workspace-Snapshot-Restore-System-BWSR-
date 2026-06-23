import subprocess
import os
import sys
from models.schema import SessionSnapshot

class SessionRestorer:
    def __init__(self, session_path: str):
        self.session_path = session_path

    def get_browser_executable(self, browser_name: str) -> str:
        executables = {
            "chrome": "google-chrome",
            "brave": "brave-browser",
            "edge": "microsoft-edge",
            "firefox": "firefox"
        }

        # Checking for WSL based on platform / release without using os.uname directly on Windows
        is_wsl = False
        if sys.platform != "win32":
            try:
                with open('/proc/version', 'r') as f:
                    if 'microsoft' in f.read().lower():
                        is_wsl = True
            except Exception:
                pass

        if sys.platform == "win32" or is_wsl:
            windows_executables = {
                "chrome": "chrome.exe",
                "brave": "brave.exe",
                "edge": "msedge.exe",
                "firefox": "firefox.exe"
            }
            return windows_executables.get(browser_name, executables.get(browser_name, browser_name))

        return executables.get(browser_name, browser_name)

    def restore(self):
        if not os.path.exists(self.session_path):
            print(f"Session file not found: {self.session_path}")
            return

        snapshot = SessionSnapshot.from_json(self.session_path)
        print(f"Restoring session from {snapshot.machine} captured at {snapshot.timestamp}")

        for browser_session in snapshot.browsers:
            executable = self.get_browser_executable(browser_session.browser)
            print(f"Restoring {browser_session.browser} using {executable}...")

            for window in browser_session.windows:
                cmd = [executable]

                if window.incognito:
                    if browser_session.browser == "firefox":
                        cmd.append("--private-window")
                    else:
                        cmd.append("--incognito")

                if browser_session.browser != "firefox":
                    cmd.append("--new-window")

                urls = [tab.url for tab in sorted(window.tabs, key=lambda t: t.position)]
                cmd.extend(urls)

                print(f"Running command: {' '.join(cmd)}")
                try:
                    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                except FileNotFoundError:
                    print(f"Error: Executable {executable} not found. Please ensure it is in your PATH.")
                except Exception as e:
                    print(f"Error launching {executable}: {e}")
