#!/usr/bin/env bash
# Local-only CGI bridge from the browser forms to the existing Bash features.
set -u

WEB_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
ARCHIVE_SERVER_ROOT="$(cd -- "$WEB_DIR/.." && pwd)"
export ARCHIVE_SERVER_ROOT

declare -A FORM=()
BODY=''

url_decode() {
    local input="${1//+/ }" output='' byte
    while [[ "$input" == *%* ]]; do
        output+="${input%%\%*}"
        input="${input#*%}"
        if [[ "$input" =~ ^([0-9A-Fa-f]{2})(.*)$ ]]; then
            printf -v byte '%b' "\\x${BASH_REMATCH[1]}"
            output+="$byte"
            input="${BASH_REMATCH[2]}"
        else
            output+='%'
        fi
    done
    REPLY="$output$input"
}

parse_form() {
    local pair key value
    local -a pairs=()
    IFS='&' read -r -a pairs <<< "$BODY"
    for pair in "${pairs[@]}"; do
        [[ "$pair" == *=* ]] || continue
        key="${pair%%=*}"
        value="${pair#*=}"
        url_decode "$key"; key="$REPLY"
        url_decode "$value"; value="$REPLY"
        FORM["$key"]="$value"
    done
}

html_escape() {
    sed 's/\&/\&amp;/g; s/</\&lt;/g; s/>/\&gt;/g; s/"/\&quot;/g'
}

if [[ "${REQUEST_METHOD:-GET}" == POST ]]; then
    length="${CONTENT_LENGTH:-0}"
    if [[ ! "$length" =~ ^[0-9]+$ ]] || (( length > 8192 )); then
        printf 'Status: 413 Payload Too Large\r\nContent-Type: text/plain; charset=utf-8\r\n\r\nRequest too large.\n'
        exit 0
    fi
    if (( length > 0 )); then IFS= read -r -N "$length" BODY; fi
elif [[ "${REQUEST_METHOD:-GET}" != GET ]]; then
    printf 'Status: 405 Method Not Allowed\r\nContent-Type: text/plain; charset=utf-8\r\n\r\nUse GET or POST.\n'
    exit 0
fi
parse_form

# Source definitions without starting the interactive terminal menu.
# shellcheck source=../../scripts/archive_server.sh
source "$ARCHIVE_SERVER_ROOT/scripts/archive_server.sh"

WEB_INPUTS=()
case "${FORM[action]:-}" in
    create) WEB_INPUTS=("${FORM[source]:-}" "${FORM[name]:-}"); operation=create_archive; title='Create archive';;
    list) operation=list_archives; title='Browse archives';;
    search) WEB_INPUTS=("${FORM[archive]:-}" "${FORM[query]:-}"); operation=search_archive; title='Search archive';;
    extract) WEB_INPUTS=("${FORM[archive]:-}"); operation=extract_archive; title='Extract archive';;
    backup) operation=create_backup; title='Project backup';;
    restore) WEB_INPUTS=("${FORM[backup]:-}"); operation=restore_backup; title='Restore backup';;
    disk) operation=disk_usage; title='Disk usage';;
    permissions) WEB_INPUTS=("${FORM[mode]:-}"); operation=permission_demo; title='File permissions';;
    log) operation=show_log; title='Activity log';;
    *) operation=''; title='Choose an action';;
esac

# Existing project functions ask for input with read_nonempty. Feed only the
# values sent by the specific form; never evaluate a submitted value as code.
read_nonempty() {
    local prompt="$1"
    if (( ${#WEB_INPUTS[@]} == 0 )); then
        printf 'Error: the form did not include the required input.\n'
        return 1
    fi
    REPLY="${WEB_INPUTS[0]}"
    WEB_INPUTS=("${WEB_INPUTS[@]:1}")
    if [[ -z "$REPLY" ]]; then printf 'Input cannot be empty.\n'; return 1; fi
}

RESULT=''
if [[ -n "$operation" ]]; then
    RESULT="$("$operation" 2>&1)"
else
    RESULT='Unknown action. Return to the dashboard and choose an option.'
fi

printf 'Content-Type: text/html; charset=utf-8\r\n\r\n'
cat <<'HTML'
<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Archive Server Result</title><link rel="stylesheet" href="/style.css"></head><body><header class="topbar"><div class="brand"><span class="brand-mark">EA</span><div><strong>Enterprise Archive Server</strong><small>Linux storage administration</small></div></div><a class="local-pill" href="/">DASHBOARD</a></header><main><section class="welcome"><p class="eyebrow">ACTION RESULT</p><h1>
HTML
printf '%s' "$title" | html_escape
cat <<'HTML'
</h1><p class="intro">The Bash archive server processed your request.</p></section><section class="card result-card"><pre>
HTML
printf '%s\n' "$RESULT" | html_escape
cat <<'HTML'
</pre><a class="back-link" href="/">← Back to dashboard</a></section></main></body></html>
HTML
