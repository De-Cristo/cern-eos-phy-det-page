#!/usr/bin/env python3

from pathlib import Path
import json
from datetime import datetime

WEB_ROOT = Path("/eos/user/l/lichengz/WEB-PORTAL")
EXTERNAL = WEB_ROOT / "external"
MANIFEST_DIR = EXTERNAL / "manifests"

REPO = Path("/eos/user/l/lichengz/cern-eos-phy-det-page")
DOCS_EXTERNAL_INDEX = REPO / "docs" / "external-index.md"

BASE_URL = "https://cms-phy-det-analysis.docs.cern.ch"

def collect_files(root: Path):
    files = []
    if not root.exists():
        return files

    for p in sorted(root.rglob("*")):
        if p.is_file():
            rel = p.relative_to(WEB_ROOT)
            files.append({
                "path": str(rel),
                "url": f"{BASE_URL}/{rel}",
                "size_bytes": p.stat().st_size,
                "modified": datetime.fromtimestamp(p.stat().st_mtime).isoformat(timespec="seconds"),
            })
    return files

def main():
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)

    daily = collect_files(EXTERNAL / "daily-html")
    artifacts = collect_files(EXTERNAL / "artifacts")

    manifest = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "daily_html": daily,
        "artifacts": artifacts,
    }

    manifest_path = MANIFEST_DIR / "external-files.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    DOCS_EXTERNAL_INDEX.parent.mkdir(parents=True, exist_ok=True)

    lines = []
    lines.append("# External Files Index")
    lines.append("")
    lines.append("This page is generated from files stored directly in `WEB-PORTAL/external/`.")
    lines.append("")
    lines.append("These files are not stored in the GitHub repository.")
    lines.append("")

    lines.append("## Daily HTML Logs")
    lines.append("")
    if daily:
        lines.append("| File | Modified | Size |")
        lines.append("|---|---:|---:|")
        for f in daily:
            lines.append(f"| [{f['path']}]({f['url']}) | {f['modified']} | {f['size_bytes']} |")
    else:
        lines.append("No daily HTML logs found yet.")
    lines.append("")

    lines.append("## Artifacts")
    lines.append("")
    if artifacts:
        lines.append("| File | Modified | Size |")
        lines.append("|---|---:|---:|")
        for f in artifacts:
            lines.append(f"| [{f['path']}]({f['url']}) | {f['modified']} | {f['size_bytes']} |")
    else:
        lines.append("No external artifacts found yet.")
    lines.append("")

    DOCS_EXTERNAL_INDEX.write_text("\n".join(lines), encoding="utf-8")

    print(f"Wrote manifest: {manifest_path}")
    print(f"Wrote MkDocs index: {DOCS_EXTERNAL_INDEX}")

if __name__ == "__main__":
    main()
