import json
import urllib.request
import urllib.error
import websocket
from typing import List, Optional, Dict, Any
from models.schema import BrowserSession, WindowSession, TabSession

class BaseCollector:
    def __init__(self, browser_name: str):
        self.browser_name = browser_name

    def collect(self) -> Optional[BrowserSession]:
        """
        Collects the session data for the browser.
        Returns a BrowserSession object if successful, or None if collection fails.
        """
        raise NotImplementedError("collect() must be implemented by subclasses")

    def _fetch_version_info(self, debug_port: int) -> Optional[Dict[str, Any]]:
        url = f"http://localhost:{debug_port}/json/version"
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=2) as response:
                return json.loads(response.read().decode())
        except (urllib.error.URLError, ConnectionRefusedError):
            return None

    def _fetch_cdp_targets_with_ws(self, ws_url: str) -> Optional[List[dict]]:
        try:
            ws = websocket.create_connection(ws_url, timeout=2)

            # Fetch targets
            req = {"id": 1, "method": "Target.getTargets"}
            ws.send(json.dumps(req))
            res = json.loads(ws.recv())
            targets = res.get("result", {}).get("targetInfos", [])

            # For each target, try to get window ID
            target_to_window = {}
            for target in targets:
                if target.get("type") == "page":
                    target_id = target.get("targetId")
                    req = {"id": 2, "method": "Browser.getWindowForTarget", "params": {"targetId": target_id}}
                    ws.send(json.dumps(req))

                    # We might get responses out of order, or events, so wait for id=2
                    window_id = None
                    while True:
                        msg = json.loads(ws.recv())
                        if msg.get("id") == 2:
                            window_id = msg.get("result", {}).get("windowId")
                            break
                    if window_id is not None:
                        target_to_window[target_id] = window_id

            ws.close()

            # Merge windowId into targets
            for target in targets:
                if target.get("targetId") in target_to_window:
                    target["windowId"] = target_to_window[target["targetId"]]

            return targets
        except Exception as e:
            return None

    def _build_session_from_cdp(self, targets: List[dict], browser_version: str = "unknown") -> BrowserSession:
        """
        Builds a BrowserSession from CDP targets.
        Groups targets by windowId and browserContextId.
        """
        # Group by windowId. If no windowId, put in default group.
        windows_map: Dict[Any, WindowSession] = {}

        # A browserContextId other than the default usually means incognito/alternative profile
        # Since we just want to flag incognito=True for non-default:
        # Default usually lacks browserContextId or has a specific one.

        for i, target in enumerate(targets):
            if target.get("type") == "page":
                url = target.get("url", "")
                if url and not url.startswith("chrome-extension://") and not url.startswith("devtools://"):
                    window_id = target.get("windowId", "default")
                    browser_context_id = target.get("browserContextId")

                    incognito = bool(browser_context_id)

                    if window_id not in windows_map:
                        windows_map[window_id] = WindowSession(incognito=incognito, tabs=[])

                    # In case multiple contexts share a windowId (unlikely but possible),
                    # we keep the window marked incognito if any tab is.
                    if incognito:
                        windows_map[window_id].incognito = True

                    tab = TabSession(
                        url=url,
                        title=target.get("title", ""),
                        position=len(windows_map[window_id].tabs)
                    )
                    windows_map[window_id].tabs.append(tab)

        return BrowserSession(
            browser=self.browser_name,
            browser_version=browser_version,
            windows=list(windows_map.values())
        )
