# Baseline Variance Report

Generated UTC: 2026-02-20T01:33:29Z
Total runs summarized: 10

| Condition | Runs | Success Rate | Latency Mean (ms) | Latency Std (ms) | Tokens In Mean | Tokens In Std | Tokens Out Mean | Tokens Out Std | Cost Mean (USD) | Cost Std (USD) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| baseline-react | 5 | 1.000 | 0.000 | 0.000 | 144.000 | 0.000 | 14.000 | 0.000 | 0.00000000 | 0.00000000 |
| baseline-single-path | 5 | 1.000 | 0.000 | 0.000 | 21.000 | 0.000 | 1.000 | 0.000 | 0.00000000 | 0.00000000 |

## Notes
- Current sweep uses deterministic scripted adapters for harness validation.
- Non-zero variance is expected once real model/provider adapters are enabled.
