from datetime import date, timedelta

from database.db_manager import Database


class CalibrationService:

    def __init__(self):
        self.db = Database()

    # =========================================================
    # Add Calibration Record
    # =========================================================

    def add_calibration(
        self,
        instrument_code,
        calibration_date,
        calibration_type,
        agency,
        certificate_number,
        cost,
        result,
        remarks,
        certificate_path
    ):
        cursor = self.db.cursor

        try:
            self.db.conn.execute("BEGIN")

            cursor.execute(
                """
                SELECT id, frequency
                FROM instruments
                WHERE instrument_code=?
                """,
                (instrument_code,)
            )

            instrument = cursor.fetchone()
            if not instrument:
                raise Exception("Instrument not found.")

            instrument_id, frequency = instrument
            calibration_date_obj = self._parse_date(calibration_date)
            next_due_date = self._calculate_next_due_date(
                calibration_date_obj,
                frequency
            )

            cursor.execute(
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
                )
                VALUES (?,?,?,?,?,?,?,?,?,?,?)
                """,
                (
                    instrument_id,
                    calibration_date_obj.isoformat(),
                    next_due_date.isoformat(),
                    calibration_type,
                    agency,
                    certificate_number,
                    cost,
                    result,
                    remarks,
                    certificate_path,
                    date.today().isoformat()
                )
            )

            self.db.conn.commit()
        except Exception:
            self.db.conn.rollback()
            raise

    # =========================================================
    # Get Calibration History
    # =========================================================

    def get_calibration_history(self, instrument_code=None):
        cursor = self.db.cursor

        sql = """
            SELECT
                i.instrument_code,
                m.machine_code,
                ch.calibration_date,
                ch.next_due_date,
                ch.calibration_type,
                ch.agency,
                ch.certificate_number,
                ch.result,
                ch.cost,
                ch.certificate_path
            FROM calibration_history ch
            JOIN instruments i ON i.id = ch.instrument_id
            LEFT JOIN machines m ON m.id = i.machine_id
        """

        params = []
        if instrument_code:
            sql += "\n            WHERE i.instrument_code = ?"
            params.append(instrument_code)

        sql += "\n            ORDER BY ch.calibration_date DESC"

        cursor.execute(sql, tuple(params))
        return cursor.fetchall()

    # =========================================================
    # Helpers
    # =========================================================

    def _get_calibration_history_columns(self):
        cursor = self.db.cursor
        cursor.execute("PRAGMA table_info(calibration_history)")
        return [row[1] for row in cursor.fetchall()]

    def _parse_date(self, value):
        if isinstance(value, date):
            return value

        if not isinstance(value, str):
            raise Exception("Invalid calibration date format.")

        try:
            return date.fromisoformat(value)
        except ValueError:
            raise Exception("Invalid calibration date format. Use YYYY-MM-DD.")

    def _calculate_next_due_date(self, calibration_date, frequency):
        period_type, value = self._frequency_to_period(frequency)

        if period_type == "days":
            return calibration_date + timedelta(days=value)

        return self._add_months(calibration_date, value)

    def _frequency_to_period(self, frequency):
        if not isinstance(frequency, str):
            raise Exception("Instrument frequency is not set.")

        normalized = frequency.strip().lower()
        mapping = {
            "weekly": ("days", 7),
            "monthly": ("months", 1),
            "quarterly": ("months", 3),
            "1 month": ("months", 1),
            "3 months": ("months", 3),
            "6 months": ("months", 6),
            "12 months": ("months", 12),
            "annually": ("months", 12),
            "yearly": ("months", 12),
        }

        if normalized not in mapping:
            raise Exception(
                f"Unsupported frequency '{frequency}'. Supported frequencies are: {', '.join(sorted(set(k.title() for k in mapping)))}."
            )

        return mapping[normalized]

    def _add_months(self, source_date, months):
        month = source_date.month - 1 + months
        year = source_date.year + month // 12
        month = month % 12 + 1
        day = min(
            source_date.day,
            self._last_day_of_month(year, month)
        )
        return date(year, month, day)

    def _last_day_of_month(self, year, month):
        if month == 12:
            return 31
        next_month = date(year, month + 1, 1)
        return (next_month - date.resolution).day
