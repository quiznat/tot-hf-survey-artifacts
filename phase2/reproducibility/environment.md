# Environment Pinning (Draft)

Last updated: 2026-02-20

## Runtime Targets
- OS: macOS (local development) + Ubuntu (CI target)
- Python: TBD
- Node.js: TBD

## Required Pins (To Fill Before Benchmarks)
- Agent framework package + version
- Model/provider SDK + version
- Supporting libraries (evaluation, parsing, logging)
- Any external tool dependencies used by agents

## Determinism Controls
- Random seed policy
- Prompt template version pinning
- Tool timeout and retry policy
- Budget cap configuration

## Change Policy
Any dependency or prompt template change must increment config version and be logged in `phase2/reproducibility/run-log.md`.
