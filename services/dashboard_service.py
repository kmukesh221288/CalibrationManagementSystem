from datetime import datetime, timedelta
from database.db_manager import Database


class DashboardService:

    def __init__(self):
        self.db = Database()

    def get_counts(self):

        cursor = self.db.cursor

        cursor.execute("SELECT COUNT(*) FROM machines")
        machines = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM instruments")
        instruments = cursor.fetchone()[0]

        today = datetime.today().date()
        next7 = today + timedelta(days=7)

        cursor.execute("SELECT due_date FROM calibration_history")

        due_today = 0
        due_next7 = 0
        overdue = 0

        for row in cursor.fetchall():

            if not row[0]:
                continue

            try:
                due = datetime.strptime(str(row[0])[:10], "%Y-%m-%d").date()
            except:
                continue

            if due < today:
                overdue += 1
            elif due == today:
                due_today += 1
            elif due <= next7:
                due_next7 += 1

        return {
            "machines": machines,
            "instruments": instruments,
            "due_today": due_today,
            "due_next7": due_next7,
            "overdue": overdue
        }

    def get_upcoming_calibrations(self):

        cursor = self.db.cursor

        cursor.execute("""
        SELECT
            m.machine_name,
            i.instrument_name,
            h.due_date
        FROM calibration_history h
        JOIN instruments i
            ON h.instrument_id = i.id
        JOIN machines m
            ON i.machine_id = m.id
        ORDER BY h.due_date
        LIMIT 15
        """)

        return cursor.fetchall()

    def close(self):
        self.db.close()