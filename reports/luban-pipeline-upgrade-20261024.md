# Luban Pipeline Upgrade

## Scope

Version 0.4.0 extends the deterministic TTE router into an evidence-gated, resumable research pipeline.
The eight TTE_CC specialist boundaries remain unchanged.

## Changes

- Added a capability registry and runtime Skill resolver using explicit or conventional installation roots.
- Added a project-local `research-state.json` with phase status, handoffs, and next actions.
- Added evidence, design, pilot, feedback, and intake artifacts.
- Added `proceed`, `downgrade`, and `stop` pilot gates before a full estimate.
- Added structured feedback classes for data, design, assumptions, null results, positive results, and pilot failure.
- Suppressed premature TTE specialist selection during literature-led question discovery.
- Added behavior tests for route leakage, portable resolution, state recovery, pilot gates, and artifact readiness.
- Replaced public-package absolute paths with runtime discovery and project-relative references.

## Verification

- Route and pipeline unit tests: 17/17 passed.
- Trigger evaluation: 14/14 passed.
- Skill structure validation: passed without warnings.
- Installed TTE_CC and research Skill resolution: found through runtime roots.
- Public package path scan: no machine-specific absolute path remains.

## Evidence boundary

The upgrade creates and validates the orchestration layer. It does not claim that literature retrieval,
clinical data analysis, estimation, or emulation diagnostics have been run for a cardiovascular cohort.
