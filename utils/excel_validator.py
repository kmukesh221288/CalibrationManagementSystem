from pathlib import Path
import pandas as pd


class ExcelValidator:

    REQUIRED_COLUMNS = [
        "Machine/Equip. Code",
        "Machine Name",
        "Instrument Code",
        "Instrument Name",
        "Department",
        "Calibration Date",
        "Calibration Due Date",
        "Frequency"
    ]

    def validate(self, excel_path, sheet_name="Internal Calibration List"):

        if not Path(excel_path).exists():
            return False, "Excel file not found."

        try:
            df = pd.read_excel(
                excel_path,
                sheet_name=sheet_name,
                header=4
            )
        except Exception as exc:
            return False, str(exc)

        df = df.dropna(how="all")

        missing = []
        for column in self.REQUIRED_COLUMNS:
            if column not in df.columns:
                missing.append(column)

        if missing:
            return False, "Missing Columns:\n" + "\n".join(missing)

        return True, df