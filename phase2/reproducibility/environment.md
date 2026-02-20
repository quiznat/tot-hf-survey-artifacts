# Environment Pinning (Draft)

Last updated: 2026-02-20

## Runtime Targets
- OS: macOS (local development) + Ubuntu (CI target)
- Stack decision: Python-first baseline/evaluation harness
- Python: 3.9.6 (local reference runtime)
- Node.js: not required for current baseline scaffold

## Required Pins (To Fill Before Benchmarks)
- Agent framework package + version
- Model/provider adapter profile:
  - Hugging Face Inference adapter implemented in `phase2/code/src/phase2_baselines/adapters.py`
  - Default config profile in `phase2/code/configs/hf-default.json`
  - Credential env var: `HF_TOKEN`
- Supporting libraries (evaluation, parsing, logging)
- Any external tool dependencies used by agents

## Determinism Controls
- Random seed policy
- Prompt template version pinning
- Tool timeout and retry policy
- Budget cap configuration

## Change Policy
Any dependency or prompt template change must increment config version and be logged in `phase2/reproducibility/run-log.md`.
