# MTD LLM Harvester: Wiki & Guides

Comprehensive technical documentation, repository layout, pipeline details, and environment setup for the MTD LLM Harvester.

---

## Project Subsystems & Repository Layout

The MTD LLM Harvester is organized as a monorepo consisting of three main components:

1. **`mtd-harvester/`**: A Python CLI tool (managed with `uv`) that crawls CERN Confluence, converts HTML to clean markdown, and exports notes to the raw vault directory.
2. **`obsidian-llm-wiki-local/`**: A Git submodule implementing the "LLM Wiki" compiler, which extracts concepts from raw notes and synthesizes them into an interlinked knowledge base.
3. **`mtd-vault/`**: The knowledge vault containing both raw source documents (`raw/docs/`) and generated Obsidian-style wiki pages (`wiki/`).

### Repository Tree
```
.
├── .gitlab-ci.yml           # 3-stage CI: harvest → compile → pages
├── .gitmodules              # Submodule configuration for the OLW engine
├── lychee.toml              # Link checker configuration
├── mtd-harvester/           # Confluence REST API crawler CLI
│   ├── pyproject.toml
│   └── src/mtd_harvester/
│       ├── config.py        # Immutably loads environment variables
│       ├── confluence.py    # REST crawler using a BFS queue
│       ├── render.py        # Crash-safe atomic markdown writer
│       └── cli.py           # Command line entry points
├── mtd-vault/               # Knowledge vault (raw and compiled md files)
│   ├── wiki.toml            # Pipeline configuration
│   ├── raw/docs/            # Raw harvested docs (CO2, Safety, Interlock, etc.)
│   └── wiki/                # LLM-synthesized concept articles & sources
└── obsidian-llm-wiki-local/ # OLW engine submodule
```

---

## The Three-Stage LLM Wiki Pipeline

The compilation pipeline operates in three distinct stages, following the Andrej Karpathy "LLM Wiki" pattern:

| Stage | Command | Model Tier | Description |
| :--- | :--- | :--- | :--- |
| **Ingest** | `olw ingest` | Fast (3–8B params, e.g. `gemma4:e4b`) | Analyzes raw notes, extracts concepts/aliases, assigns quality scores, writes summaries to `wiki/sources/`. |
| **Compile** | `olw compile` | Heavy (7–14B params, e.g. `qwen2.5:14b`) | Gathers source notes for each concept, drafts cross-referenced articles with `[[wikilinks]]` in `wiki/.drafts/`. |
| **Approve** | `olw review`/`approve` | Human review or `--auto-approve` | Reviews and approves drafted articles, removing metadata and moving them to the production `wiki/` directory. |

---

## Environment Setup & Configuration

### Required Environment Variables

| Variable | Default Value | Description |
| :--- | :--- | :--- |
| `MTD_CONFLUENCE_TOKEN` | *None* (Required) | Confluence Personal Access Token. |
| `MTD_CONFLUENCE_BASE` | `https://confluence.cern.ch` | Confluence API base URL. |
| `MTD_SEED_PAGE_IDS` | `446758929` | Seed page ID to start BFS crawl. |
| `MTD_CRAWL_CHILDREN` | `true` | Recursively follow child pages. |
| `MTD_VAULT` | `../../mtd-vault` | Path to the target vault directory. |
| `OLLAMA_URL` | `http://128.141.171.21:11434` | Shared Ollama server API endpoint. |

### Vault Pipeline Settings (`wiki.toml`)
Configure the pipeline behaviors within `mtd-vault/wiki.toml`:
```toml
[models]
fast = "gemma4:latest"
heavy = "gemma4:latest"

[ollama]
url = "http://localhost:11434"
timeout = 600
fast_ctx = 16384
heavy_ctx = 32768

[pipeline]
auto_approve = true
auto_commit = false
auto_maintain = false
```

---

## Operational Guide

### 1. Local Development & Crawling
Run the crawler manually or invoke the full pipeline (harvesting + compiling) using `uv`:
```bash
# Navigate to harvester
cd mtd-harvester
export MTD_CONFLUENCE_TOKEN="your_personal_access_token"

# Harvest Confluence pages only (writes to mtd-vault/raw/docs/)
uv run mtd-harvest confluence

# Run full pipeline (harvest + compile)
uv run mtd-harvest all
```

### 2. Manual OLW Compilation
Compile the raw notes using the OLW engine directly:
```bash
cd obsidian-llm-wiki-local
uv sync --group dev
uv run olw run --vault ../mtd-vault --auto-approve
```

### 3. Local LLM Setup
If running models locally via Ollama:
```bash
# Start local Ollama server
ollama serve

# Pull required models
ollama pull gemma4:latest

# Trigger pipeline
uv run mtd-harvest all
```

### 4. Link Validation
Use the `lychee` link checker to validate links in generated markdown files:
```bash
lychee --config lychee.toml "mtd-vault/wiki/**/*.md"
```

