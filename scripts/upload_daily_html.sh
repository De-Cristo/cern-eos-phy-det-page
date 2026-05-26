#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 3 ]; then
  echo "Usage:"
  echo "  scripts/upload_daily_html.sh PROJECT_NAME YYYY-MM-DD /path/to/log.html"
  exit 1
fi

PROJECT="$1"
DATE="$2"
SRC="$3"

YEAR="${DATE:0:4}"
TARGET_DIR="/eos/user/l/lichengz/WEB-PORTAL/external/daily-html/$PROJECT/$YEAR"
TARGET_FILE="$TARGET_DIR/$DATE.html"

if [ ! -f "$SRC" ]; then
  echo "Error: source file does not exist: $SRC"
  exit 1
fi

mkdir -p "$TARGET_DIR"
cp "$SRC" "$TARGET_FILE"

echo "Uploaded:"
echo "$TARGET_FILE"
echo
echo "URL:"
echo "https://cms-phy-det-analysis.docs.cern.ch/external/daily-html/$PROJECT/$YEAR/$DATE.html"
