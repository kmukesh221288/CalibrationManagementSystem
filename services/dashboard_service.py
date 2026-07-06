from datetime import date

from database.db_manager import Database


class DashboardService:

    def __init__(self):
        self.db = Database()

    def get_total_instruments(self):
        cursor = self.db.cursor
        cursor.execute("SELECT COUNT(*) FROM instruments")
        return cursor.fetchone()[0]

    def get_total_calibrations(self):
        cursor = self.db.cursor
        cursor.execute("SELECT COUNT(*) FROM calibration_history")
        return cursor.fetchone()[0]

    def get_due_this_month(self):
        cursor = self.db.cursor
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM calibration_history
            WHERE next_due_date BETWEEN date('now', 'start of month')
                AND date('now', 'start of month', '+1 month', '-1 day')
            """
        )
        return cursor.fetchone()[0]

    def get_overdue_count(self):
        cursor = self.db.cursor
        cursor.execute(
            "SELECT COUNT(*) FROM calibration_history WHERE next_due_date < date('now')"
        )
        return cursor.fetchone()[0]

    def get_certificate_count(self):
        cursor = self.db.cursor
        cursor.execute(
            "SELECT COUNT(*) FROM calibration_history WHERE certificate_path IS NOT NULL AND certificate_path != ''"
        )
        return cursor.fetchone()[0]

    def get_total_cost(self):
        cursor = self.db.cursor
        cursor.execute(
            "SELECT IFNULL(SUM(cost), 0) FROM calibration_history"
        )
        return cursor.fetchone()[0]
