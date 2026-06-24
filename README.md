# Browser Workspace Snapshot & Restore (BWSR)

Capture open browser windows and tabs on one Windows machine and restore them on another.

## Features

* Capture open browser sessions via Chrome DevTools Protocol (CDP)
* Preserve window grouping and organization
* Support Incognito/Private windows
* Export sessions to portable JSON files
* Restore sessions across machines
* Works natively on Windows and from WSL

### Preserved

* Browser type
* Window structure
* Open URLs
* Incognito/Private mode

### Not Preserved

* Logins and cookies
* Form data
* Scroll position
* Browser memory/state

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Launch browsers with remote debugging enabled:

```bash
chrome.exe --remote-debugging-port=9222
```

Default ports:

| Browser | Port |
| ------- | ---- |
| Chrome  | 9222 |
| Brave   | 9223 |
| Edge    | 9224 |
| Firefox | 9225 |

## Usage

### Capture

```bash
python main.py capture
```

Save to a custom file:

```bash
python main.py capture --output backup.json
```

### Restore

```bash
python main.py restore
```

Restore from a custom file:

```bash
python main.py restore --input backup.json
```

## Architecture

* **Collector** – Reads browser sessions via CDP/WebSockets
* **Exporter** – Saves sessions as JSON
* **Restorer** – Reopens browser windows and tabs
* **Models** – Dataclass-based session schema

## Testing

```bash
python -m unittest discover tests
```
