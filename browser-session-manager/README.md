# Browser Workspace Snapshot & Restore System (BWSR)

Capture the currently open browser workspace on a Windows machine and restore it later on another Windows machine (or WSL).

## Overview

The system captures URLs and window organization using the Chrome DevTools Protocol (CDP) for Chromium-based browsers, and exports them to a portable JSON file. It can then restore these sessions on another machine by launching browser windows with the captured URLs.

The system does NOT attempt to preserve:
- Login sessions
- Cookies
- Browser memory state
- Form contents
- Scroll positions
- Running JavaScript state

## Prerequisites

For the collector to work, your browsers must be launched with remote debugging enabled. For example, for Chrome:

```bash
chrome.exe --remote-debugging-port=9222
```

Ports:
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
This will create a file at `sessions/session.json`.

### 2. Restore Session

On the destination machine, run:

```bash
python main.py restore
```

By default, it looks for the `sessions/session.json` file. You can also specify a custom path using `--input` and `--output`.

## Architecture

- **Collector**: Uses CDP to extract open windows and tabs.
- **Exporter**: Writes session data to `session.json`.
- **Restorer**: Reads `session.json` and launches browsers via `subprocess`.
- **Data Model**: Defined in `models/schema.py` using `dataclasses`.
