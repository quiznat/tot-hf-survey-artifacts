# Protocol v2 Matrix Execution Checklist

Status date: 2026-02-20  
Protocol: `TOT-HF-P2-EPV2-2026-02-20`  
Task panel: `phase2/benchmarks/panels/game24_lockset_v1.json`  
Conditions: `single,react,tot` (`tot_evaluator_mode=model_self_eval`)  
Parallelism: `--max-workers 8`  
Seed policy: `--seed-policy item_hash`  
Sampling controls: `--hf-temperature 0.0`, `--hf-top-p 1.0`
Locked run artifacts dir: `phase2/benchmarks/runs/protocol_v2_locked/`  
Locked run log: `phase2/reproducibility/run-log-protocol-v2.md`

## Primary Matrix (Required)

| Model ID | Status | Report MD | Report JSON | Notes |
|---|---|---|---|---|
| `Qwen/Qwen3-Coder-Next:novita` | complete | `phase2/benchmarks/analysis/game24_lockset_report_qwen3codernext.md` | `phase2/benchmarks/analysis/game24_lockset_report_qwen3codernext.json` | executed 2026-02-20 at `--max-workers 8` |
| `Qwen/Qwen2.5-72B-Instruct` | complete | `phase2/benchmarks/analysis/game24_lockset_report_qwen25_72b.md` | `phase2/benchmarks/analysis/game24_lockset_report_qwen25_72b.json` | executed 2026-02-20 at `--max-workers 8` |
| `Qwen/Qwen2.5-Coder-32B-Instruct` | complete | `phase2/benchmarks/analysis/game24_lockset_report_qwen25_coder32b.md` | `phase2/benchmarks/analysis/game24_lockset_report_qwen25_coder32b.json` | executed 2026-02-20 at `--max-workers 8` |

## Canonical Batch Command Template

```bash
source /Users/quiznat/.zprofile
PYTHONPATH=/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/src \
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/run_game24_lockset.py \
  --provider hf \
  --model-id "<MODEL_ID>" \
  --conditions single,react,tot \
  --tot-evaluator-mode model_self_eval \
  --hf-temperature 0.0 \
  --hf-top-p 1.0 \
  --seed-policy item_hash \
  --max-workers 8 \
  --limit 50 \
  --runs-dir /Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/runs/protocol_v2_locked \
  --run-log /Users/quiznat/Desktop/Tree_of_Thought/phase2/reproducibility/run-log-protocol-v2.md \
  --confidence-level 0.95 \
  --bootstrap-samples 10000 \
  --report-md "<REPORT_MD>" \
  --report-json "<REPORT_JSON>"
```

## Completion Criteria

- All 3 model rows marked complete or replaced with documented fallback model IDs.
- Report artifacts exist for every completed model.
- `phase2/reproducibility/run-log.md` appended by manifests from all matrix runs.
- `phase2/manuscript/PREPAPER.md` updated with matrix-level summary and tradeoff interpretation.
