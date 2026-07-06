from pathlib import Path
import pandas as pd

from database.db_manager import Database
from utils.excel_validator import ExcelValidator


class ImportService:

    def __init__(self):

        self.db = Database()
        self.validator = ExcelValidator()

        self.machine_count = 0
        self.instrument_count = 0
        self.history_count = 0

    # -------------------------------------------------

    def import_file(self, excel_path):

        status, result = self.validator.validate(excel_path)

        if not status:

            raise Exception(result)

        df = result

        print(f"Rows Found : {len(df)}")

        for _, row in df.iterrows():

            self.process_row(row)

        self.db.conn.commit()

        print("\nImport Completed")
        print("-------------------------")
        print(f"Machines     : {self.machine_count}")
        print(f"Instruments  : {self.instrument_count}")
        print(f"History      : {self.history_count}")

    # -------------------------------------------------

    def process_row(self, row):

        machine_id = self.get_machine(row)

        instrument_id = self.get_instrument(
            machine_id,
            row
        )

        self.add_history(
            instrument_id,
            row
        )

    # -------------------------------------------------

    def get_machine(self, row):

        machine_code = self.clean(
            row["Machine/Equip. Code"]
        )

        machine_name = self.clean(
            row["Machine Name"]
        )

        department = self.clean(
            row["Department"]
        )

        self.db.cursor.execute(
            """
            SELECT id
            FROM machines
            WHERE machine_code=?
            """,
            (machine_code,)
        )

        machine = self.db.cursor.fetchone()

        if machine:

            return machine[0]

        self.db.cursor.execute(
            """
            INSERT INTO machines(
                machine_code,
                machine_name,
                department
            )
            VALUES(?,?,?)
            """,
            (
                machine_code,
                machine_name,
                department
            )
        )

        self.machine_count += 1

        return self.db.cursor.lastrowid

    # -------------------------------------------------

    def get_instrument(
        self,
        machine_id,
        row
    ):

        instrument_code = self.clean(
            row["Instrument Code"]
        )

        self.db.cursor.execute(
            """
            SELECT id
            FROM instruments
            WHERE instrument_code=?
            """,
            (instrument_code,)
        )

        instrument = self.db.cursor.fetchone()

        if instrument:

            return instrument[0]

        instrument_name = self.clean(
            row["Instrument Name"]
        )

        accuracy = self.clean(
            row["Accuracy/Least count"]
        )

        master = self.clean(
            row["Master Instrument used"]
        )

        frequency = self.clean(
            row["Frequency"]
        )

        self.db.cursor.execute(
            """
            INSERT INTO instruments(

                machine_id,

                instrument_code,

                instrument_name,

                accuracy,

                master_instrument,

                frequency

            )

            VALUES(?,?,?,?,?,?)

            """,
            (
                machine_id,
                instrument_code,
                instrument_name,
                accuracy,
                master,
                frequency
            )
        )

        self.instrument_count += 1

        return self.db.cursor.lastrowid

    # -------------------------------------------------

    def add_history(
        self,
        instrument_id,
        row
    ):

        calibration = self.clean_date(
            row["Calibration Date"]
        )

        due = self.clean_date(
            row["Calibration Due Date"]
        )

        remark = self.clean(
            row["Remark"]
        )

        comments = self.clean(
            row["Comments"]
        )

        self.db.cursor.execute(
            """
            INSERT INTO calibration_history(

                instrument_id,

                calibration_date,

                next_due_date,

                remark,

                comments

            )

            VALUES(?,?,?,?,?)

            """,
            (
                instrument_id,
                calibration,
                due,
                remark,
                comments
            )
        )

        self.history_count += 1

    # -------------------------------------------------

    def clean(self, value):

        if pd.isna(value):

            return ""

        return str(value).strip()

    # -------------------------------------------------

    def clean_date(self, value):

        if pd.isna(value):

            return None

        return str(value)