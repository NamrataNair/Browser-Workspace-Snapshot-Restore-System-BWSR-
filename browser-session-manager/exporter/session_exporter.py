import platform
from datetime import datetime
from typing import List
from models.schema import SessionSnapshot, BrowserSession

class SessionExporter:
    def __init__(self, output_path: str):
        self.output_path = output_path

    def export(self, browser_sessions: List[BrowserSession]) -> SessionSnapshot:
        machine_name = platform.node()
        timestamp = datetime.now().isoformat()

        snapshot = SessionSnapshot(
            machine=machine_name,
            timestamp=timestamp,
            browsers=browser_sessions
        )

        snapshot.to_json(self.output_path)
        return snapshot
