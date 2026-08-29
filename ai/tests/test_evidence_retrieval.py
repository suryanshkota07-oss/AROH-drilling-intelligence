import json
import tempfile
import unittest
from pathlib import Path

from ai.analogue_matching import WellNotFoundError
from ai.evidence_retrieval import build_risk_explanations, retrieve_evidence


DATA_DIR = Path(__file__).resolve().parents[2] / "data"


class EvidenceRetrievalTests(unittest.TestCase):
    def test_returns_only_dataset_backed_fields_for_predicted_risks(self):
        records = retrieve_evidence("AROH-ACT-01")

        self.assertEqual({record["well_id"] for record in records}, {"AROH-OFF-101", "AROH-OFF-102"})
        for record in records:
            self.assertTrue({"well_id", "event_id", "event_type", "event_depth", "formation", "severity", "relevance_score"} <= record.keys())
            self.assertGreater(record["relevance_score"], 0)
            self.assertEqual(record["data_classification"], "synthetic_demo")
            self.assertIn("Synthetic report", record["source_summary"])

    def test_ui_explanations_group_supporting_wells_and_patterns(self):
        explanations = build_risk_explanations("AROH-ACT-01")

        lost_circulation = next(item for item in explanations if item["event_type"] == "lost_circulation")
        self.assertEqual(lost_circulation["supporting_wells"], ["AROH-OFF-102"])
        self.assertIn("evidence-backed historical", lost_circulation["historical_pattern"])
        self.assertTrue(lost_circulation["evidence"])

    def test_missing_evidence_source_is_not_returned(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            test_data_dir = Path(temporary_directory)
            for path in DATA_DIR.glob("*.json"):
                records = [] if path.name == "evidence_records.json" else json.loads(path.read_text(encoding="utf-8"))
                (test_data_dir / path.name).write_text(json.dumps(records), encoding="utf-8")

            records = retrieve_evidence("AROH-ACT-01", data_dir=test_data_dir)

        self.assertEqual(records, [])

    def test_invalid_well_id_is_rejected(self):
        with self.assertRaisesRegex(WellNotFoundError, "Unknown well_id: MISSING"):
            retrieve_evidence("MISSING")


if __name__ == "__main__":
    unittest.main()
