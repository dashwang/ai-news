#!/bin/bash
#
# AI News Publisher - Daily Automation (V6)
# Schedule: 7:00 AM Asia/Shanghai (UTC+8)
#
# Steps:
#   1. fetch_news.js      - Fetch today's AI news (uses TZ for date)
#   2. agent-proper.js    - Translate using KiloClaw LLM, generate HTML
#   3. agent.js --publish - Publish to WeChat draft
#

set -e

export TZ=Asia/Shanghai

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_DIR="${SCRIPT_DIR}/data"
LOG_FILE="${LOG_DIR}/cron-$(date +%Y-%m-%d).log"
DATE=""
DRY_RUN=false

# Parse args
while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run|--dryrun) DRY_RUN=true; shift ;;
    --date=*) DATE="${1#*=}"; shift ;;
    -h|--help)
      echo "Usage: $0 [--dry-run] [--date=YYYY-MM-DD]"
      exit 0
      ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

# Default date (Shanghai)
DATE="${DATE:-$(date +%Y-%m-%d)}"

# Colors
if [ -t 1 ]; then
  G='\033[0;32m'; B='\033[0;34m'; Y='\033[1;33m'; R='\033[0;31m'; N='\033[0m'
else G='';B='';Y='';R='';N=''; fi

log() { echo -e "[${B}$(date '+%Y-%m-%d %H:%M:%S')${N}] $1" | tee -a "$LOG_FILE"; }
ok() { log "${G}✓ $1${N}"; }
warn() { log "${Y}⚠ $1${N}"; }
err() { log "${R}✗ $1${N}"; }

# Load env
[ -f "${SCRIPT_DIR}/.env" ] && { set -a; . "${SCRIPT_DIR}/.env" 2>/dev/null; set +a; ok "Env loaded"; } || warn "No .env"

check_config() {
  if [ -z "$WECHAT_APP_ID" ] || [ -z "$WECHAT_APP_SECRET" ]; then
    err "Missing WECHAT_APP_ID/SECRET"
    return 1
  fi
  ok "Config OK"
  return 0
}

fetch() {
  ok "Fetching news for ${DATE}"
  cd "${SCRIPT_DIR}"
  if $DRY_RUN; then log "[DRY-RUN] NEWS_DATE=${DATE} node fetch_news.js"; return 0; fi
  # Pass date via env var (fetch_news.js uses process.env.NEWS_DATE)
  NEWS_DATE="${DATE}" node fetch_news.js 2>&1 | tee -a "$LOG_FILE" || { err "Fetch failed"; return 1; }
  ok "Fetched"
  return 0
}

translate() {
  ok "Translating"
  cd "${SCRIPT_DIR}"
  $DRY_RUN && { log "[DRY-RUN] node agent-proper.js"; return 0; }
  node agent-proper.js --date="${DATE}" --limit=15 2>&1 | tee -a "$LOG_FILE" || { err "Translate failed"; return 1; }
  ok "Translated"
  return 0
}

publish() {
  ok "Publishing"
  cd "${SCRIPT_DIR}"
  PUBLISHED="${LOG_DIR}/published.json"
  if [ -f "$PUBLISHED" ] && grep -q "\"date\":\"${DATE}\"" "$PUBLISHED" 2>/dev/null; then
    warn "Already published, skipping"
    return 0
  fi
  $DRY_RUN && { log "[DRY-RUN] node agent.js --publish"; return 0; }
  node agent.js --publish --date="${DATE}" 2>&1 | tee -a "$LOG_FILE" || { err "Publish failed"; return 1; }
  ok "Published"
  return 0
}

summary() {
  echo ""
  log "Summary:"
  HTML="${LOG_DIR}/wechat-html-${DATE}.html"
  [ -f "$HTML" ] && log "  HTML: ${HTML} ($(wc -c < "$HTML" 2>/dev/null || echo 0) bytes)"
  PUBLISHED="${LOG_DIR}/published.json"
  [ -f "$PUBLISHED" ] && {
    MID=$(grep -A2 "\"date\":\"${DATE}\"" "$PUBLISHED" 2>/dev/null | grep draftId | head -1 | awk -F'"' '{print $4}' || true)
    [ -n "$MID" ] && log "  Media ID: ${MID}"
  }
  echo ""
}

main() {
  ok "AI News Publisher started"
  log "Date: ${DATE} (TZ=Asia/Shanghai)"
  $DRY_RUN && log "DRY-RUN mode"
  mkdir -p "$LOG_DIR"

  check_config || exit 1

  fetch || exit 1
  translate || exit 1
  publish || exit 1

  echo ""
  ok "All done (3/3)"
  summary

  find "$LOG_DIR" -name "cron-*.log" -mtime +7 -delete 2>/dev/null || true
}

trap 'err "Failed (exit $?)"' EXIT
main
trap - EXIT
