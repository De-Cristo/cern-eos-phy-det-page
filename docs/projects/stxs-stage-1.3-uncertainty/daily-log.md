# STXS Stage 1.3 Uncertainty: Daily Log

Chronological progress, task logs, and decisions for the STXS Stage 1.3 Uncertainty project.

## Interactive HTML Development Logs
These detailed logs, plots, and design reports are hosted directly on EOS:

### May 2026
*   **2026-05-28**: [Condor LHE Scratch Staging](https://cms-phy-det-analysis.docs.cern.ch/external/daily-html/stxs-stage-1.3-uncertainty/2026/2026-05-28-condor-lhe-scratch-staging.html) (HTML)
*   **2026-05-26**: [Dual Gridpack LHE Mixing Design](https://cms-phy-det-analysis.docs.cern.ch/external/daily-html/stxs-stage-1.3-uncertainty/2026/2026-05-26-dual-gridpack-lhe-mixing-design.html) (HTML)
*   **2026-05-26**: [HTML Daily Log Design](https://cms-phy-det-analysis.docs.cern.ch/external/daily-html/stxs-stage-1.3-uncertainty/2026/2026-05-26-html-daily-log-design.html) (HTML)
*   **2026-05-26**: [HTML Daily Logs Summary](https://cms-phy-det-analysis.docs.cern.ch/external/daily-html/stxs-stage-1.3-uncertainty/2026/2026-05-26-html-daily-logs.html) (HTML)
*   **2026-05-26**: [Dynamic Config Plan](https://cms-phy-det-analysis.docs.cern.ch/external/daily-html/stxs-stage-1.3-uncertainty/2026/2026-05-26-dynamic_config_plan.html) (HTML)
*   **2026-05-26**: [Stage 1.3 Upgrade Plan](https://cms-phy-det-analysis.docs.cern.ch/external/daily-html/stxs-stage-1.3-uncertainty/2026/2026-05-26-stage1p3_upgrade_plan.html) (HTML)
*   **2026-05-25**: [LHE Generation Pipeline Changelog](https://cms-phy-det-analysis.docs.cern.ch/external/daily-html/stxs-stage-1.3-uncertainty/2026/2026-05-25-lhe-generation-pipeline-changelog.html) (HTML)
*   **2026-05-25**: [LHE Generation Pipeline Design](https://cms-phy-det-analysis.docs.cern.ch/external/daily-html/stxs-stage-1.3-uncertainty/2026/2026-05-25-lhe-generation-pipeline-design.html) (HTML)
*   **2026-05-25**: [LHE Generation Pipeline Run](https://cms-phy-det-analysis.docs.cern.ch/external/daily-html/stxs-stage-1.3-uncertainty/2026/2026-05-25-lhe-generation-pipeline.html) (HTML)

### April 2026
*   **2026-04-09**: [Condor Job Flag Propagation Design](https://cms-phy-det-analysis.docs.cern.ch/external/daily-html/stxs-stage-1.3-uncertainty/2026/2026-04-09-condor-job-flag-propagation-design.html) (HTML)
*   **2026-04-09**: [Condor Job Flag Propagation Run](https://cms-phy-det-analysis.docs.cern.ch/external/daily-html/stxs-stage-1.3-uncertainty/2026/2026-04-09-condor-job-flag-propagation.html) (HTML)
*   **2026-04-08**: [Plot Refinements](https://cms-phy-det-analysis.docs.cern.ch/external/daily-html/stxs-stage-1.3-uncertainty/2026/2026-04-08-plot-refinements.html) (HTML)
*   **2026-04-08**: [Upgrade Plot](https://cms-phy-det-analysis.docs.cern.ch/external/daily-html/stxs-stage-1.3-uncertainty/2026/2026-04-08-upgrad_plot.html) (HTML)

---

## Logbook Entries

### 2026-05-28
*   **Tasks**: Fixed the Condor LHE generation workflow where downloaded/unpacked gridpack files were polluting the submit directory. Mirrored the fix in VHSTXSUnc and VH_gitlab.
*   **Decisions**: Enforce runtime inside Condor scratch (`$_CONDOR_SCRATCH_DIR`), fallback to temp scratch under `/tmp`, and create a second disposable per-job runtime scratch directory with `mktemp -d` to execute the gridpack.
*   **Next Steps**: Verify generated wrappers and regression tests on other workflows.

### 2026-05-26
*   **Tasks**: Initialized the project space and uploaded the 12 HTML daily logs to EOS.
*   **Decisions**: Standardized directory structure for project-specific logs.
*   **Next Steps**: Set up the initial workspace configuration and list relevant theoretical papers.
