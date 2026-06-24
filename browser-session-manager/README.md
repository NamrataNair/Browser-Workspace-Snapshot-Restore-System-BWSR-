# Browser Workspace Snapshot & Restore System (BWSR)

Capture the currently open browser workspace on a Windows machine and restore it later on another Windows machine (or natively in WSL via aliases).

## Overview

The system captures URLs and window organization using the Chrome DevTools Protocol (CDP) through WebSockets for Chromium-based browsers, and exports them to a portable JSON file. It can then restore these sessions on another machine by launching browser windows with the captured URLs.

The architecture is fully scalable and extensible to other browsers that support remote debugging. It is built in standard Python without relying on Docker.

The system preserves:
- The running browser details
- Open Windows and grouping
- URLs inside the window
- Incognito/Private window modes

The system does NOT attempt to preserve:
- Login sessions
- Cookies
- Browser memory state
- Form contents
- Scroll positions
- Running JavaScript state

## Prerequisites

Install the requirements before running the code.

```bash
pip install -r requirements.txt
```

For the collector to work, your browsers must be launched with remote debugging enabled. For example, for Chrome on Windows:

```bash
chrome.exe --remote-debugging-port=9222
```

Ports configured by default in `config/browsers.yaml`:
- Chrome: 9222
- Brave: 9223
- Edge: 9224
- Firefox: 9225

## Usage

### 1. Capture Session

Run the capture command to take a snapshot of your open browser sessions:

```bash
python main.py capture
```
This will read the open browsers via CDP and create a file at `sessions/session.json`.

You can also specify a custom path using `--output`:
```bash
python main.py capture --output my_backup.json
```

### 2. Restore Session

On the destination machine, ensure you have the python environment set up, and run:

```bash
python main.py restore
```

By default, it looks for the `sessions/session.json` file. You can specify a custom input file using `--input`:

```bash
python main.py restore --input my_backup.json
```

## Architecture

- **Collector**: Uses CDP and WebSockets (`collector/base.py`) to extract open windows and tabs, inferring their `windowId` and contexts to correctly map normal vs Incognito groupings.
- **Exporter**: Writes session dataclasses to `session.json`.
- **Restorer**: Reads `session.json` and launches browsers via `subprocess`. Handily proxies Linux calls to Windows executables when run from a WSL environment.
- **Data Model**: Defined in `models/schema.py` using robust Python `dataclasses`.

## Testing

You can run the test suite by executing:
```bash
python -m unittest discover tests
```
Test execution results are also attached to the repository inside `test_results.txt`.