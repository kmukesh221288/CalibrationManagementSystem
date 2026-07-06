from database.db_manager import Database


class ReminderService:

    def __init__(self):
        self.db = Database()

    def get_reminder_counts(self):
        cursor = self.db.cursor

        cursor.execute(
            "SELECT COUNT(*) FROM calibration_history WHERE next_due_date < date('now')"
        )
        overdue = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM calibration_history WHERE next_due_date BETWEEN date('now') AND date('now', '+30 days')"
        )
        due_within_30_days = cursor.fetchone()[0]

        if overdue == 0 and due_within_30_days == 0:
            return None

        return overdue, due_within_30_days
