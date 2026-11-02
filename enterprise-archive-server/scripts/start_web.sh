#!/usr/bin/env bash
# Start the optional website on loopback only so it is not exposed to a network.
set -eu
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname -- "$SCRIPT_DIR")"
WEB_DIR="$ROOT_DIR/web"
PORT="${1:-8080}"

if ! command -v busybox >/dev/null 2>&1; then
    echo 'BusyBox is required for the optional local web demo.'
    echo 'Install it in Ubuntu with: sudo apt update && sudo apt install busybox'
    exit 1
fi
if [[ ! "$PORT" =~ ^[0-9]{1,5}$ ]] || (( PORT < 1024 || PORT > 65535 )); then
    echo 'Choose an available port between 1024 and 65535.'
    exit 1
fi
chmod +x "$ROOT_DIR/scripts/archive_server.sh" "$WEB_DIR/cgi-bin/archive.cgi"
echo "Website: http://127.0.0.1:$PORT"
echo 'Keep this terminal open while using the website. Press Ctrl+C to stop it.'
exec busybox httpd -f -v -p "127.0.0.1:$PORT" -h "$WEB_DIR"
