import json
import tempfile
import unittest
from pathlib import Path

from ai.analogue_matching import WellNotFoundError
from ai.risk_ahead import assess_risks


DATA_DIR = Path(__file__).resolve().parents[2] / "data"


class RiskAheadTests(unittest.TestCase):
    def test_returns_traceable_risks_for_relevant_historical_events(self):
        risks = assess_risks("AROH-ACT-01")

        self.assertEqual({risk["event_type"] for risk in risks}, {"partial_lost_circulation", "lost_circulation"})
        for risk in risks:
            self.assertGreater(risk["risk_score"], 0)
            self.assertIn(risk["severity"], {"normal", "watch", "elevated", "critical"})
            self.assertGreater(risk["predicted_interval"]["end_md_m"], 2870)
            self.assertGreater(risk["confidence"], 0)
            self.assertTrue(risk["supporting_wells"])
            self.assertTrue(risk["supporting_wells"][0]["evidence_ids"])
            self.assertEqual(risk["data_classification"], "synthetic_demo")

    def test_missing_drilling_samples_excludes_parameter_factor_without_failing(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            test_data_dir = Path(temporary_directory)
            for path in DATA_DIR.glob("*.json"):
                records = [] if path.name == "drilling_samples.json" else json.loads(path.read_text(encoding="utf-8"))
                (test_data_dir / path.name).write_text(json.dumps(records), encoding="utf-8")

            risk = assess_risks("AROH-ACT-01", data_dir=test_data_dir)[0]

        factor = next(item for item in risk["score_factors"] if item["factor"] == "drilling_parameter_similarity")
        self.assertEqual(factor["status"], "unavailable_excluded_from_score")

    def test_no_evidence_backed_events_returns_no_risks(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            test_data_dir = Path(temporary_directory)
            for path in DATA_DIR.glob("*.json"):
                records = [] if path.name == "evidence_records.json" else json.loads(path.read_text(encoding="utf-8"))
                (test_data_dir / path.name).write_text(json.dumps(records), encoding="utf-8")

            risks = assess_risks("AROH-ACT-01", data_dir=test_data_dir)

        self.assertEqual(risks, [])

    def test_invalid_well_id_is_rejected(self):
        with self.assertRaisesRegex(WellNotFoundError, "Unknown well_id: MISSING"):
            assess_risks("MISSING")


if __name__ == "__main__":
    unittest.main()
