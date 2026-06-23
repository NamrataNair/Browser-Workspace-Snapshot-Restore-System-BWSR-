import json
from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class TabSession:
    url: str
    title: str = ""
    position: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "url": self.url,
            "title": self.title,
            "position": self.position
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TabSession":
        return cls(
            url=data.get("url", ""),
            title=data.get("title", ""),
            position=data.get("position", 0)
        )


@dataclass
class WindowSession:
    incognito: bool = False
    tabs: List[TabSession] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "incognito": self.incognito,
            "tabs": [tab.to_dict() for tab in self.tabs]
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WindowSession":
        return cls(
            incognito=data.get("incognito", False),
            tabs=[TabSession.from_dict(t) for t in data.get("tabs", [])]
        )


@dataclass
class BrowserSession:
    browser: str
    browser_version: str = "unknown"
    windows: List[WindowSession] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "browser": self.browser,
            "browser_version": self.browser_version,
            "windows": [win.to_dict() for win in self.windows]
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BrowserSession":
        return cls(
            browser=data.get("browser", "unknown"),
            browser_version=data.get("browser_version", "unknown"),
            windows=[WindowSession.from_dict(w) for w in data.get("windows", [])]
        )


@dataclass
class SessionSnapshot:
    machine: str
    timestamp: str
    browsers: List[BrowserSession] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "machine": self.machine,
            "timestamp": self.timestamp,
            "browsers": [b.to_dict() for b in self.browsers]
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SessionSnapshot":
        return cls(
            machine=data.get("machine", "unknown"),
            timestamp=data.get("timestamp", ""),
            browsers=[BrowserSession.from_dict(b) for b in data.get("browsers", [])]
        )

    def to_json(self, filepath: str):
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=4)

    @classmethod
    def from_json(cls, filepath: str) -> "SessionSnapshot":
        with open(filepath, 'r') as f:
            data = json.load(f)
        return cls.from_dict(data)
