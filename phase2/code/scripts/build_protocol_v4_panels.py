#!/usr/bin/env python3
"""Generate protocol-v4 lockset panels disjoint from pre-v4 tuned panels."""

from __future__ import annotations

import argparse
from fractions import Fraction
import itertools
import json
from pathlib import Path
import random
from typing import Any, Dict, Iterable, List, Sequence, Set, Tuple


ROOT = Path("/Users/quiznat/Desktop/Tree_of_Thought/phase2")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build protocol-v4 benchmark panels")
    parser.add_argument("--seed", type=int, default=20260301, help="Base RNG seed")
    parser.add_argument("--items-per-panel", type=int, default=50, help="Items per task panel")
    parser.add_argument(
        "--out-dir",
        default=str(ROOT / "benchmarks/panels"),
        help="Panel output directory",
    )
    parser.add_argument(
        "--reference-panels",
        default=",".join(
            [
                str(ROOT / "benchmarks/panels/game24_lockset_v1.json"),
                str(ROOT / "benchmarks/panels/subset_sum_lockset_v1.json"),
                str(ROOT / "benchmarks/panels/linear2_lockset_v1.json"),
                str(ROOT / "benchmarks/panels/digit_permutation_lockset_v1.json"),
            ]
        ),
        help="Comma-separated panel JSON files used to enforce disjointness",
    )
    parser.add_argument(
        "--disjoint-report-md",
        default=str(ROOT / "benchmarks/analysis/protocol_v4_panel_disjointness.md"),
        help="Markdown disjointness report path",
    )
    parser.add_argument(
        "--disjoint-report-json",
        default=str(ROOT / "benchmarks/analysis/protocol_v4_panel_disjointness.json"),
        help="JSON disjointness report path",
    )
    return parser.parse_args()


def _game24_signature(numbers: Sequence[int]) -> Tuple[int, int, int, int]:
    vals = tuple(sorted(int(x) for x in numbers))
    if len(vals) != 4:
        raise RuntimeError("game24 signature requires exactly 4 numbers")
    return vals


def _subset_sum_signature(payload: Dict[str, Any]) -> Tuple[Tuple[int, ...], int]:
    numbers = tuple(sorted(int(x) for x in payload["numbers"]))
    target = int(payload["target"])
    return numbers, target


def _linear2_signature(payload: Dict[str, Any]) -> Tuple[Tuple[float, float, float], Tuple[float, float, float]]:
    equations = payload["equations"]
    if not isinstance(equations, list) or len(equations) != 2:
        raise RuntimeError("linear2 payload requires exactly 2 equations")
    eq_rows = []
    for row in equations:
        if not isinstance(row, list) or len(row) != 3:
            raise RuntimeError("linear2 equation rows must have length 3")
        eq_rows.append((float(row[0]), float(row[1]), float(row[2])))
    eq_rows.sort()
    return eq_rows[0], eq_rows[1]


def _digit_perm_signature(payload: Dict[str, Any]) -> Tuple[Tuple[int, int, int, int], int]:
    digits = tuple(sorted(int(x) for x in payload["digits"]))
    if len(digits) != 4:
        raise RuntimeError("digit-permutation signature requires 4 digits")
    divisor = int(payload["divisor"])
    return digits, divisor


def _extract_task_signature(task_id: str, item: Dict[str, Any]) -> Any:
    if task_id == "game24-demo":
        raw = item.get("input_data", item.get("numbers"))
        if not isinstance(raw, list):
            raise RuntimeError("game24 item must include input_data list")
        return _game24_signature(raw)
    if task_id == "subset-sum-demo":
        payload = item.get("input_data")
        if not isinstance(payload, dict):
            raise RuntimeError("subset-sum item must include input_data object")
        return _subset_sum_signature(payload)
    if task_id == "linear2-demo":
        payload = item.get("input_data")
        if not isinstance(payload, dict):
            raise RuntimeError("linear2 item must include input_data object")
        return _linear2_signature(payload)
    if task_id == "digit-permutation-demo":
        payload = item.get("input_data")
        if not isinstance(payload, dict):
            raise RuntimeError("digit-permutation item must include input_data object")
        return _digit_perm_signature(payload)
    raise RuntimeError(f"Unsupported task_id: {task_id}")


def _load_reference_signatures(paths: Iterable[Path]) -> Dict[str, Set[Any]]:
    signatures: Dict[str, Set[Any]] = {
        "game24-demo": set(),
        "subset-sum-demo": set(),
        "linear2-demo": set(),
        "digit-permutation-demo": set(),
    }
    for path in paths:
        if not path.exists():
            raise RuntimeError(f"Reference panel missing: {path}")
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise RuntimeError(f"Reference panel malformed: {path}")
        task_id = str(payload.get("task_id", "")).strip()
        if not task_id:
            panel_id = str(payload.get("panel_id", "")).strip().lower()
            file_name = path.name.lower()
            if "game24" in panel_id or "game24" in file_name:
                task_id = "game24-demo"
            elif "subset" in panel_id or "subset" in file_name:
                task_id = "subset-sum-demo"
            elif "linear2" in panel_id or "linear2" in file_name:
                task_id = "linear2-demo"
            elif "digit-permutation" in panel_id or "digit_permutation" in file_name:
                task_id = "digit-permutation-demo"
        if task_id not in signatures:
            continue
        items = payload.get("items", [])
        if not isinstance(items, list):
            raise RuntimeError(f"Reference panel items malformed: {path}")
        for item in items:
            if not isinstance(item, dict):
                continue
            signatures[task_id].add(_extract_task_signature(task_id, item))
    return signatures


def _eval_expr(expr: str) -> Fraction | None:
    try:
        value = eval(expr, {"__builtins__": {}}, {})
    except Exception:
        return None
    if isinstance(value, Fraction):
        return value
    if isinstance(value, int):
        return Fraction(value, 1)
    return None


def _solve_game24(numbers: Sequence[int]) -> str | None:
    start = [(Fraction(int(n), 1), str(int(n))) for n in numbers]

    def recurse(terms: List[Tuple[Fraction, str]]) -> str | None:
        if len(terms) == 1:
            if terms[0][0] == Fraction(24, 1):
                return terms[0][1]
            return None

        for i in range(len(terms)):
            for j in range(i + 1, len(terms)):
                a_val, a_expr = terms[i]
                b_val, b_expr = terms[j]
                rest = [terms[k] for k in range(len(terms)) if k not in (i, j)]

                candidates: List[Tuple[Fraction, str]] = [
                    (a_val + b_val, f"({a_expr}+{b_expr})"),
                    (a_val - b_val, f"({a_expr}-{b_expr})"),
                    (b_val - a_val, f"({b_expr}-{a_expr})"),
                    (a_val * b_val, f"({a_expr}*{b_expr})"),
                ]
                if b_val != 0:
                    candidates.append((a_val / b_val, f"({a_expr}/{b_expr})"))
                if a_val != 0:
                    candidates.append((b_val / a_val, f"({b_expr}/{a_expr})"))

                for value, expr in candidates:
                    out = recurse(rest + [(value, expr)])
                    if out is not None:
                        return out
        return None

    result = recurse(start)
    if result is None:
        return None
    value = _eval_expr(result)
    if value != Fraction(24, 1):
        return None
    return result


def build_game24_panel(seed: int, n_items: int, blocked: Set[Any]) -> Dict[str, Any]:
    rng = random.Random(seed + 11)
    items: List[Dict[str, Any]] = []
    seen: Set[Any] = set()

    while len(items) < n_items:
        numbers = [rng.randint(1, 10) for _ in range(4)]
        sig = _game24_signature(numbers)
        if sig in blocked or sig in seen:
            continue
        expr = _solve_game24(numbers)
        if expr is None:
            continue
        seen.add(sig)
        item_id = f"g24-v4-{len(items)+1:03d}"
        items.append(
            {
                "item_id": item_id,
                "input_data": numbers,
                "oracle_solution": expr,
            }
        )

    return {
        "panel_id": "game24-lockset-v4",
        "task_id": "game24-demo",
        "selection_seed": seed + 11,
        "description": "Protocol-v4 confirmatory Game24 panel disjoint from v1 tuned items.",
        "disjoint_against": ["game24-lockset-v1"],
        "items": items,
    }


def build_subset_sum_panel(seed: int, n_items: int, blocked: Set[Any]) -> Dict[str, Any]:
    rng = random.Random(seed + 22)
    items: List[Dict[str, Any]] = []
    seen: Set[Any] = set()

    while len(items) < n_items:
        numbers = sorted(rng.randint(1, 25) for _ in range(rng.randint(5, 8)))
        subset_size = rng.randint(2, min(4, len(numbers)))
        subset_indices = sorted(rng.sample(range(len(numbers)), k=subset_size))
        target = sum(numbers[idx] for idx in subset_indices)
        sig = (tuple(numbers), target)
        if sig in blocked or sig in seen:
            continue
        seen.add(sig)
        chosen = [numbers[idx] for idx in subset_indices]
        item_id = f"ss-v4-{len(items)+1:03d}"
        items.append(
            {
                "item_id": item_id,
                "input_data": {"numbers": numbers, "target": target},
                "oracle_solution": ",".join(str(x) for x in chosen),
            }
        )

    return {
        "panel_id": "subset-sum-lockset-v4",
        "task_id": "subset-sum-demo",
        "selection_seed": seed + 22,
        "description": "Protocol-v4 confirmatory subset-sum panel disjoint from v1 tuned items.",
        "disjoint_against": ["subset-sum-lockset-v1"],
        "items": items,
    }


def build_linear2_panel(seed: int, n_items: int, blocked: Set[Any]) -> Dict[str, Any]:
    rng = random.Random(seed + 33)
    items: List[Dict[str, Any]] = []
    seen: Set[Any] = set()

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
        payload = {"equations": [[a, b, c], [d, e, f_val]]}
        sig = _linear2_signature(payload)
        if sig in blocked or sig in seen:
            continue
        seen.add(sig)
        item_id = f"lin-v4-{len(items)+1:03d}"
        items.append(
            {
                "item_id": item_id,
                "input_data": payload,
                "oracle_solution": f"x={x_star},y={y_star}",
            }
        )

    return {
        "panel_id": "linear2-lockset-v4",
        "task_id": "linear2-demo",
        "selection_seed": seed + 33,
        "description": "Protocol-v4 confirmatory linear-system panel disjoint from v1 tuned items.",
        "disjoint_against": ["linear2-lockset-v1"],
        "items": items,
    }


def _best_permutation(digits: Sequence[int], divisor: int) -> int | None:
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


def build_digit_permutation_panel(seed: int, n_items: int, blocked: Set[Any]) -> Dict[str, Any]:
    rng = random.Random(seed + 44)
    divisors = [3, 4, 5, 6, 7, 8, 9, 11]
    items: List[Dict[str, Any]] = []
    seen: Set[Any] = set()

    while len(items) < n_items:
        digits = [rng.randint(0, 9) for _ in range(4)]
        divisor = rng.choice(divisors)
        payload = {"digits": digits, "divisor": divisor}
        sig = _digit_perm_signature(payload)
        if sig in blocked or sig in seen:
            continue
        best = _best_permutation(digits, divisor)
        if best is None:
            continue
        seen.add(sig)
        item_id = f"perm-v4-{len(items)+1:03d}"
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
        "panel_id": "digit-permutation-lockset-v4",
        "task_id": "digit-permutation-demo",
        "selection_seed": seed + 44,
        "description": "Protocol-v4 confirmatory digit-permutation panel disjoint from v1 tuned items.",
        "disjoint_against": ["digit-permutation-lockset-v1"],
        "items": items,
    }


def _collect_signatures(task_id: str, items: List[Dict[str, Any]]) -> Set[Any]:
    out: Set[Any] = set()
    for item in items:
        out.add(_extract_task_signature(task_id, item))
    return out


def _build_disjoint_report(panels: List[Dict[str, Any]], blocked: Dict[str, Set[Any]]) -> Dict[str, Any]:
    rows: List[Dict[str, Any]] = []
    for panel in panels:
        task_id = str(panel["task_id"])
        items = panel.get("items", [])
        current = _collect_signatures(task_id, items)
        overlap = current & blocked.get(task_id, set())
        rows.append(
            {
                "task_id": task_id,
                "panel_id": panel.get("panel_id"),
                "items": len(items),
                "blocked_signature_count": len(blocked.get(task_id, set())),
                "current_signature_count": len(current),
                "overlap_count": len(overlap),
                "status": "ok" if not overlap else "overlap_detected",
            }
        )
    return {
        "generated_utc": "2026-02-22T06:00:00Z",
        "status": "ok" if all(row["overlap_count"] == 0 for row in rows) else "failed",
        "rows": rows,
    }


def main() -> int:
    args = parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    ref_paths = [Path(part.strip()) for part in str(args.reference_panels).split(",") if part.strip()]
    blocked = _load_reference_signatures(ref_paths)

    panels = [
        build_game24_panel(seed=args.seed, n_items=int(args.items_per_panel), blocked=blocked["game24-demo"]),
        build_subset_sum_panel(seed=args.seed, n_items=int(args.items_per_panel), blocked=blocked["subset-sum-demo"]),
        build_linear2_panel(seed=args.seed, n_items=int(args.items_per_panel), blocked=blocked["linear2-demo"]),
        build_digit_permutation_panel(seed=args.seed, n_items=int(args.items_per_panel), blocked=blocked["digit-permutation-demo"]),
    ]

    writes = [
        (out_dir / "game24_lockset_v4.json", panels[0]),
        (out_dir / "subset_sum_lockset_v4.json", panels[1]),
        (out_dir / "linear2_lockset_v4.json", panels[2]),
        (out_dir / "digit_permutation_lockset_v4.json", panels[3]),
    ]

    for path, panel in writes:
        path.write_text(json.dumps(panel, indent=2, sort_keys=False) + "\n", encoding="utf-8")
        print(f"wrote={path} items={len(panel['items'])} panel_id={panel['panel_id']}")

    report = _build_disjoint_report(panels=panels, blocked=blocked)
    report_json_path = Path(args.disjoint_report_json)
    report_md_path = Path(args.disjoint_report_md)
    report_json_path.parent.mkdir(parents=True, exist_ok=True)
    report_md_path.parent.mkdir(parents=True, exist_ok=True)

    report_json_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    md_lines = [
        "# Protocol v4 Panel Disjointness Report",
        "",
        f"Status: {report['status']}",
        "",
        "| Task | Panel ID | Items | Blocked Signatures | Current Signatures | Overlap | Status |",
        "|---|---|---:|---:|---:|---:|---|",
    ]
    for row in report["rows"]:
        md_lines.append(
            "| {task} | {panel} | {items} | {blocked} | {current} | {overlap} | {status} |".format(
                task=row["task_id"],
                panel=row["panel_id"],
                items=row["items"],
                blocked=row["blocked_signature_count"],
                current=row["current_signature_count"],
                overlap=row["overlap_count"],
                status=row["status"],
            )
        )
    report_md_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    print(f"disjoint_report_md={report_md_path}")
    print(f"disjoint_report_json={report_json_path}")

    if report["status"] != "ok":
        raise RuntimeError("Disjointness check failed")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
