#!/usr/bin/env bash
set -euo pipefail

SOURCE_DIR="/eos/user/l/lichengz/cern-eos-phy-det-page"
TARGET_DIR="/eos/user/l/lichengz/WEB-PORTAL"
BUILD_DIR="/tmp/lichengz/cern-eos-phy-det-page-build"
VENV="/tmp/lichengz/venvs/cern-eos-phy-det-page"

mkdir -p "$BUILD_DIR"
mkdir -p "$TARGET_DIR/external/daily-html"
mkdir -p "$TARGET_DIR/external/artifacts"
mkdir -p "$TARGET_DIR/external/manifests"

source "$VENV/bin/activate"

cd "$SOURCE_DIR"

echo "[1/4] Generating external file indexes..."
python3 scripts/index_external.py || true

echo "[2/4] Building MkDocs site into /tmp..."
rm -rf "$BUILD_DIR"
mkdocs build --site-dir "$BUILD_DIR"

echo "[3/4] Publishing generated site safely..."
rsync -av --delete \
  --exclude 'external/' \
  "$BUILD_DIR"/ "$TARGET_DIR"/

echo "[4/4] Done."
echo "Open: https://cms-phy-det-analysis.docs.cern.ch/"
