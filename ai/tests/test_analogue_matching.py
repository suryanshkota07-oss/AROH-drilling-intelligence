import json
import tempfile
import unittest
from pathlib import Path

from ai.analogue_matching import WellNotFoundError, find_analogues


DATA_DIR = Path(__file__).resolve().parents[2] / "data"


class AnalogueMatchingTests(unittest.TestCase):
    def test_ranks_formation_matched_offsets_and_returns_explanations(self):
        results = find_analogues("AROH-ACT-01")

        self.assertEqual([item["well_id"] for item in results], ["AROH-OFF-101", "AROH-OFF-102", "AROH-OFF-103"])
        self.assertGreater(results[0]["similarity_score"], results[1]["similarity_score"])
        self.assertEqual(results[0]["formation"], "Boka Sand")
        self.assertGreater(results[0]["distance"], 0)
        self.assertEqual(results[0]["relevant_historical_events"][0]["event_id"], "EVT-O101-001")
        self.assertTrue(all("explanation" in feature for feature in results[0]["matching_features"]))

    def test_missing_location_excludes_proximity_without_failing(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            test_data_dir = Path(temporary_directory)
            for path in DATA_DIR.glob("*.json"):
                records = json.loads(path.read_text(encoding="utf-8"))
                if path.name == "wells.json":
                    records[1].pop("location")
                (test_data_dir / path.name).write_text(json.dumps(records), encoding="utf-8")

            result = next(
                item for item in find_analogues("AROH-ACT-01", data_dir=test_data_dir)
                if item["well_id"] == "AROH-OFF-101"
            )

        proximity = next(item for item in result["matching_features"] if item["feature"] == "proximity")
        self.assertIsNone(result["distance"])
        self.assertEqual(proximity["status"], "unavailable_excluded_from_score")

    def test_invalid_well_id_raises_clear_error(self):
        with self.assertRaisesRegex(WellNotFoundError, "Unknown well_id: MISSING"):
            find_analogues("MISSING")


if __name__ == "__main__":
    unittest.main()
