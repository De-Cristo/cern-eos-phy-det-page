# Agent Rules for CERN EOS PHY DET Website

This repository controls the source structure of the website:

/eos/user/l/lichengz/cern-eos-phy-det-page

The public website root is:

/eos/user/l/lichengz/WEB-PORTAL

The website URL is:

https://cms-phy-det-analysis.docs.cern.ch/

## Core Architecture

The GitHub repository stores:

- MkDocs configuration
- Markdown source pages
- scripts
- templates
- navigation structure
- generated index pages

The WEB-PORTAL directory stores:

- published static website files
- uploaded daily HTML logs
- plots
- figures
- external artifacts
- generated manifests

## Critical Safety Rule

Never delete or overwrite:

/eos/user/l/lichengz/WEB-PORTAL/external/

This directory contains files that are intentionally not stored in GitHub.

## Publishing Rule

To publish the site, run:

scripts/publish.sh

Do not manually run rsync to WEB-PORTAL unless the command excludes external/.

## Allowed Agent Actions

The agent may:

- create or edit Markdown files under docs/
- create or edit scripts under scripts/
- update mkdocs.yml
- generate daily/project indexes
- run mkdocs build
- run scripts/publish.sh when explicitly asked
- upload daily HTML logs using scripts/upload_daily_html.sh
- upload artifacts using scripts/upload_artifact.sh

## Restricted Agent Actions

The agent must not:

- delete WEB-PORTAL/external/
- run rsync --delete to WEB-PORTAL without excluding external/
- put large plots, binary figures, ROOT files, or generated HTML logs into Git
- commit secrets, tokens, credentials, private EOS paths, or internal unpublished information
- fabricate analysis results
- silently overwrite daily logs
- edit access-control configuration unless explicitly asked

## Storage Policy

Small source-controlled files:

- Markdown
- YAML
- shell scripts
- Python scripts
- templates
- small documentation images if necessary

Large or generated files:

- HTML logs
- PNG/PDF plots
- generated reports
- ROOT output snapshots
- notebooks exported to HTML
- data tables

must go to:

/eos/user/l/lichengz/WEB-PORTAL/external/

## Standard Commands

Build only:

mkdocs build --site-dir /tmp/lichengz/cern-eos-phy-det-page-build

Publish safely:

scripts/publish.sh

Upload daily HTML log:

scripts/upload_daily_html.sh PROJECT_NAME YYYY-MM-DD /path/to/log.html

Upload artifacts:

scripts/upload_artifact.sh PROJECT_NAME YYYY-MM-DD file1 file2 ...

## Review Policy

Before publishing, summarize:

- files changed in Git repo
- files uploaded to WEB-PORTAL/external/
- whether mkdocs build succeeded
- final URL to check
