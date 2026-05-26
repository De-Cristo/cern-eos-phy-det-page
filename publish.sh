#!/usr/bin/env bash
set -euo pipefail

SOURCE_DIR="/eos/user/l/lichengz/cern-eos-phy-det-page"
TARGET_DIR="/eos/user/l/lichengz/WEB-PORTAL"
VENV="/tmp/lichengz/venvs/cern-eos-phy-det-page"

source "$VENV/bin/activate"

cd "$SOURCE_DIR"

echo "[1/3] Building MkDocs site..."
mkdocs build

echo "[2/3] Publishing to EOS web root..."
rsync -av --delete site/ "$TARGET_DIR/"

echo "[3/3] Done."
echo "Open: https://cms-phy-det-analysis.docs.cern.ch/"
