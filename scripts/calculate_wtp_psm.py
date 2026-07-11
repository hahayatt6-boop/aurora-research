"""Calculate Van Westendorp PSM outputs from aggregate RES-003-WTP tables.

The script intentionally accepts aggregate counts only. Do not feed respondent-
level survey exports into this tool or commit respondent-level files to git.
"""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple


PRICE_CODES: List[Tuple[str, float, Optional[float], str]] = [
    ("P00_09", 5.0, 9.0, "0-9"),
    ("P10_19", 15.0, 19.0, "10-19"),
    ("P20_29", 25.0, 29.0, "20-29"),
    ("P30_49", 40.0, 49.0, "30-49"),
    ("P50_79", 65.0, 79.0, "50-79"),
    ("P80_119", 100.0, 119.0, "80-119"),
    ("P120_199", 160.0, 199.0, "120-199"),
    ("P200_299", 250.0, 299.0, "200-299"),
    ("P300_PLUS", 300.0, None, ">=300"),
]

PRICE_INDEX = {code: idx for idx, (code, _midpoint, _upper, _label) in enumerate(PRICE_CODES)}
PSM_QUESTIONS = {"too_cheap", "cheap", "expensive", "too_expensive"}


@dataclass(frozen=True)
class Point:
    x: float
    y: float
    label: str


@dataclass(frozen=True)
class Crossing:
    value: Optional[float]
    status: str

    def formatted_value(self) -> str:
        if self.value is None:
            return ""
        if self.status == "right_censored":
            return ">=300"
        return f"{self.value:.2f}"


def read_psm_counts(path: Path) -> Dict[str, Dict[str, List[int]]]:
    """Read aggregate PSM counts keyed by scenario and question."""
    scenarios: Dict[str, Dict[str, List[int]]] = defaultdict(lambda: {q: [0] * len(PRICE_CODES) for q in PSM_QUESTIONS})
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        required = {"scenario", "psm_question", "price_code", "n"}
        missing = required.difference(reader.fieldnames or [])
        if missing:
            raise ValueError(f"{path} missing columns: {', '.join(sorted(missing))}")
        for row in reader:
            scenario = row["scenario"].strip()
            question = row["psm_question"].strip()
            price_code = row["price_code"].strip()
            if not scenario and not question and not price_code:
                continue
            if question not in PSM_QUESTIONS:
                raise ValueError(f"Unknown psm_question: {question}")
            if price_code not in PRICE_INDEX:
                raise ValueError(f"Unknown price_code: {price_code}")
            scenarios[scenario][question][PRICE_INDEX[price_code]] += int(row["n"] or 0)
    return scenarios


def cumulative_forward(counts: List[int]) -> List[float]:
    total = sum(counts)
    if total == 0:
        return [0.0] * len(counts)
    running = 0
    values = []
    for count in counts:
        running += count
        values.append(running / total)
    return values


def cumulative_reverse(counts: List[int]) -> List[float]:
    total = sum(counts)
    if total == 0:
        return [0.0] * len(counts)
    running = 0
    values = [0.0] * len(counts)
    for idx in range(len(counts) - 1, -1, -1):
        running += counts[idx]
        values[idx] = running / total
    return values


def points(values: Iterable[float]) -> List[Point]:
    return [
        Point(x=midpoint, y=value, label=label)
        for (_code, midpoint, _upper, label), value in zip(PRICE_CODES, values)
    ]


def find_crossing(left: List[Point], right: List[Point]) -> Crossing:
    """Find the first intersection, using linear interpolation where needed."""
    candidates: List[Crossing] = []
    diffs = [a.y - b.y for a, b in zip(left, right)]
    for idx, diff in enumerate(diffs):
        if abs(diff) < 1e-12:
            status = "right_censored" if left[idx].label == ">=300" else "exact"
            candidates.append(Crossing(left[idx].x, status))
    for idx in range(len(diffs) - 1):
        d1 = diffs[idx]
        d2 = diffs[idx + 1]
        if d1 == 0 or d2 == 0 or (d1 > 0) == (d2 > 0):
            continue
        x1 = left[idx].x
        x2 = left[idx + 1].x
        if left[idx + 1].label == ">=300":
            candidates.append(Crossing(x2, "right_censored"))
            continue
        ratio = abs(d1) / (abs(d1) + abs(d2))
        candidates.append(Crossing(x1 + (x2 - x1) * ratio, "interpolated"))
    if candidates:
        return candidates[0]

    closest_idx = min(range(len(diffs)), key=lambda idx: abs(diffs[idx]))
    status = "right_censored" if left[closest_idx].label == ">=300" else "closest_no_crossing"
    return Crossing(left[closest_idx].x, status)


def calculate_scenario(question_counts: Dict[str, List[int]]) -> Dict[str, Crossing | int]:
    totals = {sum(counts) for counts in question_counts.values()}
    if not totals or min(totals) == 0:
        return {
            "n_total": 0,
            "pmc": Crossing(None, "no_data"),
            "opp": Crossing(None, "no_data"),
            "pme": Crossing(None, "no_data"),
        }
    too_cheap = points(cumulative_forward(question_counts["too_cheap"]))
    cheap = points(cumulative_reverse(question_counts["cheap"]))
    expensive = points(cumulative_forward(question_counts["expensive"]))
    too_expensive = points(cumulative_forward(question_counts["too_expensive"]))
    return {
        "n_total": min(totals) if totals else 0,
        "pmc": find_crossing(too_cheap, expensive),
        "opp": find_crossing(too_cheap, too_expensive),
        "pme": find_crossing(cheap, too_expensive),
    }


def write_price_points(path: Path, scenarios: Dict[str, Dict[str, List[int]]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        fieldnames = [
            "scenario",
            "n_total",
            "pmc_cny",
            "pmc_status",
            "opp_cny",
            "opp_status",
            "pme_cny",
            "pme_status",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for scenario in sorted(scenarios):
            result = calculate_scenario(scenarios[scenario])
            pmc = result["pmc"]
            opp = result["opp"]
            pme = result["pme"]
            assert isinstance(pmc, Crossing)
            assert isinstance(opp, Crossing)
            assert isinstance(pme, Crossing)
            writer.writerow(
                {
                    "scenario": scenario,
                    "n_total": result["n_total"],
                    "pmc_cny": pmc.formatted_value(),
                    "pmc_status": pmc.status,
                    "opp_cny": opp.formatted_value(),
                    "opp_status": opp.status,
                    "pme_cny": pme.formatted_value(),
                    "pme_status": pme.status,
                }
            )


def write_demand_scenario(input_path: Path, output_path: Path) -> None:
    with input_path.open(newline="", encoding="utf-8") as input_handle, output_path.open(
        "w", newline="", encoding="utf-8"
    ) as output_handle:
        reader = csv.DictReader(input_handle)
        required = {"anchor_price_cny", "effective_n_main", "high_certainty_n", "assumed_conversion_rate"}
        missing = required.difference(reader.fieldnames or [])
        if missing:
            raise ValueError(f"{input_path} missing columns: {', '.join(sorted(missing))}")
        fieldnames = [
            "anchor_price_cny",
            "effective_n_main",
            "high_certainty_n",
            "high_certainty_pct",
            "assumed_conversion_rate",
            "conservative_demand_index",
        ]
        writer = csv.DictWriter(output_handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            effective_n = int(row["effective_n_main"] or 0)
            high_n = int(row["high_certainty_n"] or 0)
            conversion_rate = float(row["assumed_conversion_rate"] or 0)
            high_pct = high_n / effective_n if effective_n else 0.0
            writer.writerow(
                {
                    "anchor_price_cny": row["anchor_price_cny"],
                    "effective_n_main": effective_n,
                    "high_certainty_n": high_n,
                    "high_certainty_pct": f"{high_pct:.6f}",
                    "assumed_conversion_rate": f"{conversion_rate:.6f}",
                    "conservative_demand_index": f"{high_pct * conversion_rate:.6f}",
                }
            )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--psm-input", type=Path, required=True, help="Aggregate PSM distribution CSV")
    parser.add_argument("--price-output", type=Path, required=True, help="Output PSM price points CSV")
    parser.add_argument("--demand-input", type=Path, help="Optional aggregate demand scenario CSV")
    parser.add_argument("--demand-output", type=Path, help="Output demand scenario CSV")
    args = parser.parse_args()

    scenarios = read_psm_counts(args.psm_input)
    write_price_points(args.price_output, scenarios)
    if args.demand_input or args.demand_output:
        if not args.demand_input or not args.demand_output:
            raise ValueError("--demand-input and --demand-output must be provided together")
        write_demand_scenario(args.demand_input, args.demand_output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
