# Protocol v5 Smoke Results (Qwen3 Novita)

## Condition Summary

| Task | Condition | Runs | Success | Latency (ms) | Tokens In | Tokens Out |
|---|---:|---:|---:|---:|---:|---:|
| digit-permutation-demo | single | 10 | 70.0% | 9872.3 | 28.0 | 188.7 |
| digit-permutation-demo | cot | 10 | 60.0% | 7021.2 | 41.0 | 266.2 |
| digit-permutation-demo | cot_sc | 10 | 60.0% | 79578.7 | 480.0 | 2603.3 |
| digit-permutation-demo | react | 10 | 100.0% | 7274.7 | 52.0 | 152.7 |
| digit-permutation-demo | tot | 10 | 100.0% | 15513.3 | 202.0 | 6.6 |
| digit-permutation-demo | tot_gen | 10 | 100.0% | 25430.1 | 374.3 | 57.8 |
| game24-demo | single | 10 | 30.0% | 15989.7 | 21.0 | 19.3 |
| game24-demo | cot | 10 | 20.0% | 15723.4 | 34.0 | 238.4 |
| game24-demo | cot_sc | 10 | 0.0% | 80533.0 | 410.0 | 2269.0 |
| game24-demo | react | 10 | 10.0% | 8330.0 | 271.1 | 253.1 |
| game24-demo | tot | 10 | 80.0% | 65645.9 | 1198.7 | 140.4 |
| game24-demo | tot_gen | 10 | 80.0% | 91032.6 | 12606.4 | 571.3 |
| linear2-demo | single | 10 | 100.0% | 5391.2 | 30.0 | 121.0 |
| linear2-demo | cot | 10 | 100.0% | 10459.2 | 43.0 | 145.3 |
| linear2-demo | cot_sc | 10 | 100.0% | 95173.2 | 500.0 | 1514.6 |
| linear2-demo | react | 10 | 100.0% | 5524.7 | 50.0 | 133.9 |
| linear2-demo | tot | 10 | 60.0% | 79618.4 | 798.1 | 21.5 |
| linear2-demo | tot_gen | 10 | 100.0% | 32531.5 | 844.4 | 95.1 |
| subset-sum-demo | single | 10 | 50.0% | 2688.4 | 53.2 | 1.9 |
| subset-sum-demo | cot | 10 | 80.0% | 7404.5 | 66.2 | 175.4 |
| subset-sum-demo | cot_sc | 10 | 90.0% | 79124.3 | 732.0 | 2058.1 |
| subset-sum-demo | react | 10 | 70.0% | 6759.3 | 82.4 | 159.8 |
| subset-sum-demo | tot | 10 | 100.0% | 25476.7 | 382.8 | 61.8 |
| subset-sum-demo | tot_gen | 10 | 100.0% | 19763.3 | 483.3 | 64.5 |

## Full Paired Comparisons

| Task | A | B | Items | Δ(A-B) | CI | p | Holm |
|---|---:|---:|---:|---:|---:|---:|---:|
| digit-permutation-demo | cot | cot_sc | 10 | +0.000 | [+0.000, +0.000] | 1 | 1 |
| digit-permutation-demo | cot | react | 10 | -0.400 | [-0.700, -0.100] | 0.125 | 1 |
| digit-permutation-demo | cot | single | 10 | -0.100 | [-0.400, +0.200] | 1 | 1 |
| digit-permutation-demo | cot | tot | 10 | -0.400 | [-0.700, -0.100] | 0.125 | 1 |
| digit-permutation-demo | cot | tot_gen | 10 | -0.400 | [-0.700, -0.100] | 0.125 | 1 |
| digit-permutation-demo | cot_sc | react | 10 | -0.400 | [-0.700, -0.100] | 0.125 | 1 |
| digit-permutation-demo | cot_sc | single | 10 | -0.100 | [-0.400, +0.200] | 1 | 1 |
| digit-permutation-demo | cot_sc | tot | 10 | -0.400 | [-0.700, -0.100] | 0.125 | 1 |
| digit-permutation-demo | cot_sc | tot_gen | 10 | -0.400 | [-0.700, -0.100] | 0.125 | 1 |
| digit-permutation-demo | react | single | 10 | +0.300 | [+0.000, +0.600] | 0.25 | 1 |
| digit-permutation-demo | react | tot | 10 | +0.000 | [+0.000, +0.000] | 1 | 1 |
| digit-permutation-demo | react | tot_gen | 10 | +0.000 | [+0.000, +0.000] | 1 | 1 |
| digit-permutation-demo | single | tot | 10 | -0.300 | [-0.600, +0.000] | 0.25 | 1 |
| digit-permutation-demo | single | tot_gen | 10 | -0.300 | [-0.600, -0.100] | 0.25 | 1 |
| digit-permutation-demo | tot_gen | tot | 10 | +0.000 | [+0.000, +0.000] | 1 | 1 |
| game24-demo | cot | cot_sc | 10 | +0.200 | [+0.000, +0.500] | 0.5 | 1 |
| game24-demo | cot | react | 10 | +0.100 | [-0.200, +0.400] | 1 | 1 |
| game24-demo | cot | single | 10 | -0.100 | [-0.400, +0.200] | 1 | 1 |
| game24-demo | cot | tot | 10 | -0.600 | [-0.900, -0.300] | 0.03125 | 0.34375 |
| game24-demo | cot | tot_gen | 10 | -0.600 | [-0.900, -0.300] | 0.03125 | 0.34375 |
| game24-demo | cot_sc | react | 10 | -0.100 | [-0.300, +0.000] | 1 | 1 |
| game24-demo | cot_sc | single | 10 | -0.300 | [-0.600, -0.100] | 0.25 | 1 |
| game24-demo | cot_sc | tot | 10 | -0.800 | [-1.000, -0.500] | 0.0078125 | 0.117188 |
| game24-demo | cot_sc | tot_gen | 10 | -0.800 | [-1.000, -0.500] | 0.0078125 | 0.117188 |
| game24-demo | react | single | 10 | -0.200 | [-0.500, +0.000] | 0.5 | 1 |
| game24-demo | react | tot | 10 | -0.700 | [-1.000, -0.400] | 0.015625 | 0.203125 |
| game24-demo | react | tot_gen | 10 | -0.700 | [-0.900, -0.400] | 0.015625 | 0.203125 |
| game24-demo | single | tot | 10 | -0.500 | [-0.900, -0.100] | 0.125 | 1 |
| game24-demo | single | tot_gen | 10 | -0.500 | [-0.900, -0.100] | 0.125 | 1 |
| game24-demo | tot_gen | tot | 10 | +0.000 | [-0.300, +0.300] | 1 | 1 |
| linear2-demo | cot | cot_sc | 10 | +0.000 | [+0.000, +0.000] | 1 | 1 |
| linear2-demo | cot | react | 10 | +0.000 | [+0.000, +0.000] | 1 | 1 |
| linear2-demo | cot | single | 10 | +0.000 | [+0.000, +0.000] | 1 | 1 |
| linear2-demo | cot | tot | 10 | +0.400 | [+0.100, +0.700] | 0.125 | 1 |
| linear2-demo | cot | tot_gen | 10 | +0.000 | [+0.000, +0.000] | 1 | 1 |
| linear2-demo | cot_sc | react | 10 | +0.000 | [+0.000, +0.000] | 1 | 1 |
| linear2-demo | cot_sc | single | 10 | +0.000 | [+0.000, +0.000] | 1 | 1 |
| linear2-demo | cot_sc | tot | 10 | +0.400 | [+0.100, +0.700] | 0.125 | 1 |
| linear2-demo | cot_sc | tot_gen | 10 | +0.000 | [+0.000, +0.000] | 1 | 1 |
| linear2-demo | react | single | 10 | +0.000 | [+0.000, +0.000] | 1 | 1 |
| linear2-demo | react | tot | 10 | +0.400 | [+0.100, +0.700] | 0.125 | 1 |
| linear2-demo | react | tot_gen | 10 | +0.000 | [+0.000, +0.000] | 1 | 1 |
| linear2-demo | single | tot | 10 | +0.400 | [+0.100, +0.700] | 0.125 | 1 |
| linear2-demo | single | tot_gen | 10 | +0.000 | [+0.000, +0.000] | 1 | 1 |
| linear2-demo | tot_gen | tot | 10 | +0.400 | [+0.100, +0.700] | 0.125 | 1 |
| subset-sum-demo | cot | cot_sc | 10 | -0.100 | [-0.300, +0.000] | 1 | 1 |
| subset-sum-demo | cot | react | 10 | +0.100 | [-0.300, +0.500] | 1 | 1 |
| subset-sum-demo | cot | single | 10 | +0.300 | [-0.100, +0.700] | 0.375 | 1 |
| subset-sum-demo | cot | tot | 10 | -0.200 | [-0.500, +0.000] | 0.5 | 1 |
| subset-sum-demo | cot | tot_gen | 10 | -0.200 | [-0.500, +0.000] | 0.5 | 1 |
| subset-sum-demo | cot_sc | react | 10 | +0.200 | [-0.200, +0.600] | 0.625 | 1 |
| subset-sum-demo | cot_sc | single | 10 | +0.400 | [+0.100, +0.700] | 0.125 | 1 |
| subset-sum-demo | cot_sc | tot | 10 | -0.100 | [-0.300, +0.000] | 1 | 1 |
| subset-sum-demo | cot_sc | tot_gen | 10 | -0.100 | [-0.300, +0.000] | 1 | 1 |
| subset-sum-demo | react | single | 10 | +0.200 | [-0.300, +0.600] | 0.6875 | 1 |
| subset-sum-demo | react | tot | 10 | -0.300 | [-0.600, +0.000] | 0.25 | 1 |
| subset-sum-demo | react | tot_gen | 10 | -0.300 | [-0.600, +0.000] | 0.25 | 1 |
| subset-sum-demo | single | tot | 10 | -0.500 | [-0.800, -0.200] | 0.0625 | 0.9375 |
| subset-sum-demo | single | tot_gen | 10 | -0.500 | [-0.800, -0.200] | 0.0625 | 0.9375 |
| subset-sum-demo | tot_gen | tot | 10 | +0.000 | [+0.000, +0.000] | 1 | 1 |
