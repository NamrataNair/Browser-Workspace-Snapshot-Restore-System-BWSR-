import argparse
import os
import yaml
from collector.chrome import ChromeCollector
from collector.brave import BraveCollector
from collector.edge import EdgeCollector
from collector.firefox import FirefoxCollector
from exporter.session_exporter import SessionExporter
from restorer.restore import SessionRestorer

def load_config(config_path="config/browsers.yaml"):
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    return {}

def capture_session(session_file: str, config_path: str):
    print("Capturing browser session...")
    config = load_config(config_path).get('browsers', {})

    collectors = []

    # Setup collectors based on config
    if config.get('chrome', {}).get('enabled', True):
        collectors.append(ChromeCollector(debug_port=config.get('chrome', {}).get('debug_port', 9222)))
    if config.get('brave', {}).get('enabled', True):
        collectors.append(BraveCollector(debug_port=config.get('brave', {}).get('debug_port', 9223)))
    if config.get('edge', {}).get('enabled', True):
        collectors.append(EdgeCollector(debug_port=config.get('edge', {}).get('debug_port', 9224)))
    if config.get('firefox', {}).get('enabled', True):
        collectors.append(FirefoxCollector(debug_port=config.get('firefox', {}).get('debug_port', 9225)))

    browser_sessions = []
    for collector in collectors:
        session = collector.collect()
        if session:
            browser_sessions.append(session)
            print(f"Captured session for {collector.browser_name}")
        else:
            print(f"No session found for {collector.browser_name} (or remote debugging disabled)")

    if not browser_sessions:
        print("No browser sessions captured.")
        return

    exporter = SessionExporter(session_file)
    exporter.export(browser_sessions)
    print(f"Session exported to {session_file}")

def restore_session(session_file: str):
    print("Restoring browser session...")
    restorer = SessionRestorer(session_file)
    restorer.restore()
    print("Restore process initiated.")

def main():
    parser = argparse.ArgumentParser(description="Browser Workspace Snapshot & Restore System (BWSR)")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Capture command
    parser_capture = subparsers.add_parser("capture", help="Capture current browser sessions")
    parser_capture.add_argument("--output", default="sessions/session.json", help="Output session file path")
    parser_capture.add_argument("--config", default="config/browsers.yaml", help="Path to config file")

    # Restore command
    parser_restore = subparsers.add_parser("restore", help="Restore a saved browser session")
    parser_restore.add_argument("--input", default="sessions/session.json", help="Input session file path")

    args = parser.parse_args()

    # Ensure directory exists if there is one
    target_file = args.output if args.command == "capture" else args.input
    dir_name = os.path.dirname(target_file)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)

    if args.command == "capture":
        capture_session(args.output, args.config)
    elif args.command == "restore":
        restore_session(args.input)

if __name__ == "__main__":
    main()
