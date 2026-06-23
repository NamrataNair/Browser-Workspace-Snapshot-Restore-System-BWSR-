from typing import Optional
from models.schema import BrowserSession
from .base import BaseCollector

class EdgeCollector(BaseCollector):
    def __init__(self, debug_port: int = 9224):
        super().__init__("edge")
        self.debug_port = debug_port

    def collect(self) -> Optional[BrowserSession]:
        version_info = self._fetch_version_info(self.debug_port)
        if not version_info:
            return None

        ws_url = version_info.get("webSocketDebuggerUrl")
        if not ws_url:
            return None

        targets = self._fetch_cdp_targets_with_ws(ws_url)
        if targets is None:
            return None

        return self._build_session_from_cdp(targets, browser_version=version_info.get("Browser", "unknown"))
