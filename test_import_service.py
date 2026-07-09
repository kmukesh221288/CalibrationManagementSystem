import unittest
import pandas as pd

from services.import_service import ImportService


class FakeCursor:
    def __init__(self):
        self.lastrowid = 1

    def execute(self, query, params=()):
        return None

    def fetchone(self):
        return None


class FakeConnection:
    def commit(self):
        return None


class FakeDB:
    def __init__(self):
        self.conn = FakeConnection()
        self.cursor = FakeCursor()


class ImportServiceTests(unittest.TestCase):
    def test_import_file_supports_external_sheet_and_returns_summary(self):
        service = ImportService()
        service.db = FakeDB()
        service.validator.validate = lambda excel_path, sheet_name="Internal Calibration List": (
            True,
            pd.DataFrame([
                {
                    "Machine/Equip. Code": "M1",
                    "Machine Name": "Machine 1",
                    "Instrument Code": "I1",
                    "Instrument Name": "Instrument 1",
                    "Department": "Dept",
                    "Calibration Date": "2024-01-01",
                    "Calibration Due Date": "2025-01-01",
                }
            ]),
        )

        summary = service.import_file(
            "dummy.xlsx",
            sheet_name="External Calibration List",
            calibration_type="External",
        )

        self.assertEqual(summary["new_instruments"], 1)
        self.assertEqual(summary["updated"], 0)
        self.assertEqual(summary["history_created"], 1)
        self.assertEqual(summary["errors"], 0)


if __name__ == "__main__":
    unittest.main()
