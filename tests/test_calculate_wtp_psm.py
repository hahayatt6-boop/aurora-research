import csv
import tempfile
import unittest
from pathlib import Path

from scripts.calculate_wtp_psm import main


PRICE_CODES = [
    "P00_09",
    "P10_19",
    "P20_29",
    "P30_49",
    "P50_79",
    "P80_119",
    "P120_199",
    "P200_299",
    "P300_PLUS",
]


class WTPPSMCalculationTest(unittest.TestCase):
    def write_psm_fixture(self, path: Path) -> None:
        counts = {
            "too_cheap": [80, 10, 10, 0, 0, 0, 0, 0, 0],
            "cheap": [0, 0, 20, 30, 30, 20, 0, 0, 0],
            "expensive": [0, 0, 0, 20, 30, 30, 20, 0, 0],
            "too_expensive": [0, 0, 0, 0, 20, 30, 30, 20, 0],
        }
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=["scenario", "psm_question", "price_code", "n"])
            writer.writeheader()
            for question, question_counts in counts.items():
                for code, count in zip(PRICE_CODES, question_counts):
                    writer.writerow(
                        {
                            "scenario": "stated_preference",
                            "psm_question": question,
                            "price_code": code,
                            "n": count,
                        }
                    )

    def test_calculates_price_points_from_aggregate_counts(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            psm_input = root / "psm.csv"
            price_output = root / "price.csv"
            self.write_psm_fixture(psm_input)

            exit_code = main_with_args(["--psm-input", str(psm_input), "--price-output", str(price_output)])

            self.assertEqual(0, exit_code)
            with price_output.open(encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(1, len(rows))
            self.assertEqual("stated_preference", rows[0]["scenario"])
            self.assertEqual("100", rows[0]["n_total"])
            self.assertIn(rows[0]["opp_status"], {"exact", "interpolated"})
            self.assertGreater(float(rows[0]["opp_cny"]), 0)
            self.assertLess(float(rows[0]["opp_cny"]), 300)

    def test_calculates_demand_scenario_without_changing_price_points(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            psm_input = root / "psm.csv"
            demand_input = root / "demand-input.csv"
            price_output = root / "price.csv"
            demand_output = root / "demand-output.csv"
            self.write_psm_fixture(psm_input)
            demand_input.write_text(
                "anchor_price_cny,effective_n_main,high_certainty_n,assumed_conversion_rate\n"
                "39,200,50,0.3\n",
                encoding="utf-8",
            )

            exit_code = main_with_args(
                [
                    "--psm-input",
                    str(psm_input),
                    "--price-output",
                    str(price_output),
                    "--demand-input",
                    str(demand_input),
                    "--demand-output",
                    str(demand_output),
                ]
            )

            self.assertEqual(0, exit_code)
            with demand_output.open(encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual("0.250000", rows[0]["high_certainty_pct"])
            self.assertEqual("0.075000", rows[0]["conservative_demand_index"])


def main_with_args(args):
    import sys

    original_argv = sys.argv
    try:
        sys.argv = ["calculate_wtp_psm.py", *args]
        return main()
    finally:
        sys.argv = original_argv


if __name__ == "__main__":
    unittest.main()
