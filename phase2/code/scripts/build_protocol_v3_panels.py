#!/usr/bin/env python3
"""Generate deterministic lockset panels for protocol v3 tasks."""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path
import random
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build protocol-v3 benchmark panels")
    parser.add_argument(
        "--seed",
        type=int,
        default=20260222,
        help="Base RNG seed for deterministic panel generation",
    )
    parser.add_argument(
        "--items-per-panel",
        type=int,
        default=50,
        help="Number of items to generate for each panel",
    )
    parser.add_argument(
        "--out-dir",
        default="/Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/panels",
        help="Output directory for panel JSON files",
    )
    return parser.parse_args()


def build_subset_sum_panel(seed: int, n_items: int) -> dict[str, Any]:
    rng = random.Random(seed)
    items: list[dict[str, Any]] = []
    seen: set[tuple[tuple[int, ...], int]] = set()

    while len(items) < n_items:
        numbers = sorted(rng.randint(1, 20) for _ in range(rng.randint(5, 7)))
        subset_size = rng.randint(2, min(4, len(numbers)))
        subset_indices = sorted(rng.sample(range(len(numbers)), k=subset_size))
        target = sum(numbers[idx] for idx in subset_indices)
        key = (tuple(numbers), target)
        if key in seen:
            continue
        seen.add(key)
        selection = [numbers[idx] for idx in subset_indices]
        item_id = f"ss-v1-{len(items)+1:03d}"
        items.append(
            {
                "item_id": item_id,
                "input_data": {
                    "numbers": numbers,
                    "target": target,
                },
                "oracle_solution": ",".join(str(x) for x in selection),
            }
        )

    return {
        "panel_id": "subset-sum-lockset-v1",
        "task_id": "subset-sum-demo",
        "selection_seed": seed,
        "description": "Fixed subset-sum lockset for paired-condition evaluation.",
        "items": items,
    }


def build_linear2_panel(seed: int, n_items: int) -> dict[str, Any]:
    rng = random.Random(seed + 101)
    items: list[dict[str, Any]] = []
    seen: set[tuple[tuple[int, int, int], tuple[int, int, int]]] = set()

    while len(items) < n_items:
        x_star = rng.randint(-9, 9)
        y_star = rng.randint(-9, 9)

        a, b = rng.randint(-9, 9), rng.randint(-9, 9)
        d, e = rng.randint(-9, 9), rng.randint(-9, 9)
        if (a == 0 and b == 0) or (d == 0 and e == 0):
            continue
        det = (a * e) - (b * d)
        if det == 0:
            continue

        c = (a * x_star) + (b * y_star)
        f_val = (d * x_star) + (e * y_star)
        eq1 = (a, b, c)
        eq2 = (d, e, f_val)
        key = (eq1, eq2)
        if key in seen:
            continue
        seen.add(key)

        item_id = f"lin-v1-{len(items)+1:03d}"
        items.append(
            {
                "item_id": item_id,
                "input_data": {
                    "equations": [list(eq1), list(eq2)],
                },
                "oracle_solution": f"x={x_star},y={y_star}",
            }
        )

    return {
        "panel_id": "linear2-lockset-v1",
        "task_id": "linear2-demo",
        "selection_seed": seed + 101,
        "description": "Fixed 2x2 linear-system lockset for paired-condition evaluation.",
        "items": items,
    }


def _best_permutation(digits: list[int], divisor: int) -> int | None:
    best: int | None = None
    for perm in itertools.permutations(digits, 4):
        if perm[0] == 0:
            continue
        value = (perm[0] * 1000) + (perm[1] * 100) + (perm[2] * 10) + perm[3]
        if value % divisor != 0:
            continue
        if best is None or value > best:
            best = value
    return best


def build_digit_permutation_panel(seed: int, n_items: int) -> dict[str, Any]:
    rng = random.Random(seed + 202)
    divisors = [3, 4, 5, 6, 7, 8, 9, 11]
    items: list[dict[str, Any]] = []
    seen: set[tuple[tuple[int, ...], int]] = set()

    while len(items) < n_items:
        digits = [rng.randint(0, 9) for _ in range(4)]
        divisor = rng.choice(divisors)
        key = (tuple(sorted(digits)), divisor)
        if key in seen:
            continue
        best = _best_permutation(digits, divisor)
        if best is None:
            continue
        seen.add(key)
        item_id = f"perm-v1-{len(items)+1:03d}"
        items.append(
            {
                "item_id": item_id,
                "input_data": {
                    "digits": digits,
                    "divisor": divisor,
                    "oracle_max": best,
                },
                "oracle_solution": str(best),
            }
        )

    return {
        "panel_id": "digit-permutation-lockset-v1",
        "task_id": "digit-permutation-demo",
        "selection_seed": seed + 202,
        "description": "Fixed digit-permutation optimization lockset for paired-condition evaluation.",
        "items": items,
    }


def main() -> int:
    args = parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    panels = [
        (
            out_dir / "subset_sum_lockset_v1.json",
            build_subset_sum_panel(seed=args.seed, n_items=int(args.items_per_panel)),
        ),
        (
            out_dir / "linear2_lockset_v1.json",
            build_linear2_panel(seed=args.seed, n_items=int(args.items_per_panel)),
        ),
        (
            out_dir / "digit_permutation_lockset_v1.json",
            build_digit_permutation_panel(seed=args.seed, n_items=int(args.items_per_panel)),
        ),
    ]

    for path, panel in panels:
        path.write_text(json.dumps(panel, indent=2, sort_keys=False) + "\n", encoding="utf-8")
        print(f"wrote={path} items={len(panel['items'])} panel_id={panel['panel_id']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
