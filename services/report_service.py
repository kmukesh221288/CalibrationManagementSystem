import os
from datetime import datetime

from openpyxl import Workbook
from openpyxl.styles import Font

from database.db_manager import Database


class ReportService:

    def __init__(self):
        self.db = Database()

    def generate_due_calibration_report(self, department="All"):
        cursor = self.db.cursor
        cursor.execute(
            """
            SELECT
                i.instrument_code,
                m.machine_code,
                m.machine_name,
                m.department,
                h.calibration_date,
                h.next_due_date,
                CAST(julianday(h.next_due_date) - julianday(date('now')) AS INTEGER) AS days_remaining,
                CASE
                    WHEN h.next_due_date < date('now') THEN 'Overdue'
                    WHEN h.next_due_date BETWEEN date('now') AND date('now', '+30 days') THEN 'Due Soon'
                    ELSE 'Valid'
                END AS status
            FROM calibration_history h
            JOIN instruments i ON i.id = h.instrument_id
            LEFT JOIN machines m ON m.id = i.machine_id
            WHERE (? = 'All' OR m.department = ?)
            ORDER BY h.next_due_date ASC
            """,
            (department, department)
        )
        return cursor.fetchall()

    def export_to_excel(self, rows):
        os.makedirs("exports", exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Due_Calibration_Report_{timestamp}.xlsx"
        file_path = os.path.join("exports", filename)

        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Due Calibration Report"

        headers = [
            "Instrument Code",
            "Machine Code",
            "Machine Name",
            "Department",
            "Calibration Date",
            "Next Due Date",
            "Days Remaining",
            "Status",
        ]

        sheet.append(headers)
        for cell in sheet[1]:
            cell.font = Font(bold=True)

        for row in rows:
            sheet.append(list(row))

        for column in sheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                value = cell.value
                if value is None:
                    continue
                max_length = max(max_length, len(str(value)))
            sheet.column_dimensions[column_letter].width = max_length + 2

        sheet.freeze_panes = "A2"
        workbook.save(file_path)

        return os.path.abspath(file_path)
