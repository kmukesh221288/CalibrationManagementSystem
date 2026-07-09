import pandas as pd
from datetime import datetime

from database.db_manager import Database
from utils.excel_validator import ExcelValidator


class ImportService:

    def __init__(self):
        self.db = Database()
        self.validator = ExcelValidator()

        self.reset_counts()

    def reset_counts(self):
        self.new_instruments = 0
        self.updated = 0
        self.history_created = 0
        self.errors = 0

    def import_file(self, excel_path, sheet_name="Internal Calibration List", calibration_type="Internal"):
        status, result = self.validator.validate(excel_path, sheet_name=sheet_name)

        if not status:
            raise Exception(result)

        df = result
        self.reset_counts()

        print(f"Rows Found : {len(df)}")

        for _, row in df.iterrows():
            if self.is_empty_row(row):
                continue

            try:
                self.process_row(row, calibration_type=calibration_type)
            except Exception:
                self.errors += 1

        self.db.conn.commit()

        print("\nImport Completed")
        print("-------------------------")
        print(f"New Instruments : {self.new_instruments}")
        print(f"Updated         : {self.updated}")
        print(f"History         : {self.history_created}")
        print(f"Errors          : {self.errors}")

        return {
            "new_instruments": self.new_instruments,
            "updated": self.updated,
            "history_created": self.history_created,
            "errors": self.errors,
        }

    def process_row(self, row, calibration_type="Internal"):
        machine_id, _ = self.get_machine(row)
        instrument_id, is_new_instrument = self.get_instrument(machine_id, row)

        if is_new_instrument:
            self.new_instruments += 1
        else:
            self.updated += 1

        if self.add_history(instrument_id, row, calibration_type=calibration_type):
            self.history_created += 1

    def get_machine(self, row):
        machine_code = self.clean(row.get("Machine/Equip. Code", ""))
        machine_name = self.clean(row.get("Machine Name", ""))
        department = self.clean(row.get("Department", ""))

        self.db.cursor.execute(
            "SELECT id FROM machines WHERE machine_code = ?",
            (machine_code,),
        )

        machine = self.db.cursor.fetchone()
        if machine:
            return machine[0], False

        self.db.cursor.execute(
            "INSERT INTO machines (machine_code, machine_name, department) VALUES (?, ?, ?)",
            (machine_code, machine_name, department),
        )

        return self.db.cursor.lastrowid, True

    def get_instrument(self, machine_id, row):
        instrument_code = self.clean(row.get("Instrument Code", ""))

        self.db.cursor.execute(
            "SELECT id, machine_id FROM instruments WHERE instrument_code = ?",
            (instrument_code,),
        )

        instrument = self.db.cursor.fetchone()
        if instrument:
            instrument_id, existing_machine_id = instrument
            machine_code = self.clean(row.get("Machine/Equip. Code", ""))
            machine_name = self.clean(row.get("Machine Name", ""))
            department = self.clean(row.get("Department", ""))
            self.db.cursor.execute(
                "UPDATE machines SET machine_code = ?, machine_name = ?, department = ? WHERE id = ?",
                (machine_code, machine_name, department, existing_machine_id),
            )
            return instrument_id, False

        instrument_name = self.clean(row.get("Instrument Name", ""))
        accuracy = self.clean(row.get("Accuracy/Least count", ""))
        master = self.clean(row.get("Master Instrument used", ""))
        frequency = self.clean(row.get("Frequency", ""))

        self.db.cursor.execute(
            """
            INSERT INTO instruments (
                machine_id,
                instrument_code,
                instrument_name,
                accuracy,
                master_instrument,
                frequency
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (machine_id, instrument_code, instrument_name, accuracy, master, frequency),
        )

        return self.db.cursor.lastrowid, True

    def add_history(self, instrument_id, row, calibration_type="Internal"):
        calibration = self.clean_date(row.get("Calibration Date", ""))
        due = self.clean_date(row.get("Calibration Due Date", ""))

        self.db.cursor.execute(
            "SELECT id FROM calibration_history WHERE instrument_id = ? LIMIT 1",
            (instrument_id,),
        )
        if self.db.cursor.fetchone():
            return False

        self.db.cursor.execute(
            """
            INSERT INTO calibration_history (
                instrument_id,
                calibration_date,
                next_due_date,
                calibration_type,
                agency,
                certificate_number,
                cost,
                result,
                remarks,
                certificate_path,
                created_on
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                instrument_id,
                calibration,
                due,
                calibration_type,
                "",
                "",
                None,
                "",
                "",
                "",
                datetime.today().strftime("%Y-%m-%d"),
            ),
        )

        return True

    def is_empty_row(self, row):
        return all(
            self.clean(row.get(column, "")) == ""
            for column in [
                "Machine/Equip. Code",
                "Machine Name",
                "Instrument Code",
                "Instrument Name",
                "Department",
                "Calibration Date",
                "Calibration Due Date",
            ]
        )

    def clean(self, value):
        if pd.isna(value):
            return ""
        return str(value).strip()

    def clean_date(self, value):
        if value is None or pd.isna(value):
            raise ValueError("Calibration date is required.")

        parsed_date = pd.to_datetime(value, errors="coerce")
        if pd.isna(parsed_date):
            raise ValueError("Invalid calibration date.")

        return parsed_date.strftime("%Y-%m-%d")