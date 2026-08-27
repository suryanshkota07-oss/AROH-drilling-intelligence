"""Integrity checks for the AROH synthetic demonstration dataset."""

import json
import unittest
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parents[1]


def load(name: str):
    with (DATA_DIR / name).open(encoding="utf-8") as dataset_file:
        return json.load(dataset_file)


class SyntheticDatasetTests(unittest.TestCase):
    def test_all_records_are_explicitly_synthetic(self):
        for filename in (
            "wells.json",
            "formation_intervals.json",
            "drilling_samples.json",
            "drilling_events.json",
            "evidence_records.json",
            "drilling_scenarios.json",
        ):
            for record in load(filename):
                self.assertEqual(record["data_classification"], "synthetic_demo")

    def test_foreign_keys_reference_existing_records(self):
        well_ids = {well["well_id"] for well in load("wells.json")}
        events = {event["event_id"]: event for event in load("drilling_events.json")}
        evidence = {item["evidence_id"]: item for item in load("evidence_records.json")}

        for filename in ("formation_intervals.json", "drilling_samples.json", "drilling_scenarios.json"):
            for record in load(filename):
                self.assertIn(record["well_id"], well_ids)

        for event_id, event in events.items():
            self.assertIn(event["well_id"], well_ids)
            for evidence_id in event["evidence_ids"]:
                self.assertIn(evidence_id, evidence)
                self.assertEqual(evidence[evidence_id]["event_id"], event_id)

    def test_historical_loss_events_exist_for_demo_scenario(self):
        loss_events = [
            event for event in load("drilling_events.json")
            if event["event_type"] in {"partial_lost_circulation", "lost_circulation"}
            and event["formation_name"] == "Boka Sand"
        ]
        self.assertGreaterEqual(len(loss_events), 2)


if __name__ == "__main__":
    unittest.main()
