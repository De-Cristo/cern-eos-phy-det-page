#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 3 ]; then
  echo "Usage:"
  echo "  scripts/upload_artifact.sh PROJECT_NAME YYYY-MM-DD file1 [file2 ...]"
  exit 1
fi

PROJECT="$1"
DATE="$2"
shift 2

TARGET_DIR="/eos/user/l/lichengz/WEB-PORTAL/external/artifacts/$PROJECT/$DATE"
mkdir -p "$TARGET_DIR"

for SRC in "$@"; do
  if [ ! -f "$SRC" ]; then
    echo "Warning: skipping missing file: $SRC"
    continue
  fi
  cp "$SRC" "$TARGET_DIR/"
  echo "Uploaded: $TARGET_DIR/$(basename "$SRC")"
done

echo
echo "Artifact directory URL:"
echo "https://cms-phy-det-analysis.docs.cern.ch/external/artifacts/$PROJECT/$DATE/"
