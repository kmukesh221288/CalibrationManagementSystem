from database.db_manager import Database


class InstrumentService:

    def __init__(self):
        self.db = Database()

    # =========================================================
    # Get All Instruments
    # =========================================================

    def get_all_instruments(self):
        cursor = self.db.cursor

        cursor.execute("""
        SELECT

            m.machine_code,
            m.machine_name,
            i.instrument_code,
            i.instrument_name,
            m.department,
            i.frequency,
            m.status

        FROM instruments i

        JOIN machines m
            ON i.machine_id = m.id

        ORDER BY m.machine_name
        """)

        return cursor.fetchall()

    # =========================================================
    # Search Instruments
    # =========================================================

    def search_instruments(self, search_text):
        cursor = self.db.cursor

        keyword = f"%{search_text}%"

        cursor.execute("""
        SELECT

            m.machine_code,
            m.machine_name,
            i.instrument_code,
            i.instrument_name,
            m.department,
            i.frequency,
            m.status

        FROM instruments i

        JOIN machines m
            ON i.machine_id = m.id

        WHERE

            m.machine_code LIKE ?
            OR m.machine_name LIKE ?
            OR i.instrument_code LIKE ?
            OR i.instrument_name LIKE ?
            OR m.department LIKE ?
            OR i.frequency LIKE ?

        ORDER BY m.machine_name
        """,
        (
            keyword,
            keyword,
            keyword,
            keyword,
            keyword,
            keyword
        ))

        return cursor.fetchall()

    # =========================================================
    # Add Instrument
    # =========================================================

    def add_instrument(
        self,
        machine_code,
        machine_name,
        department,
        instrument_code,
        instrument_name,
        frequency
    ):
        cursor = self.db.cursor

        cursor.execute(
            """
            SELECT id
            FROM machines
            WHERE machine_code=?
            """,
            (machine_code,)
        )

        machine = cursor.fetchone()

        if machine:
            machine_id = machine[0]
        else:
            cursor.execute(
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
            machine_id = cursor.lastrowid

        cursor.execute(
            """
            SELECT id
            FROM instruments
            WHERE instrument_code=?
            """,
            (instrument_code,)
        )

        if cursor.fetchone():
            raise Exception(
                "Instrument Code already exists."
            )

        cursor.execute(
            """
            INSERT INTO instruments(

                machine_id,
                instrument_code,
                instrument_name,
                frequency

            )

            VALUES(?,?,?,?)

            """,
            (
                machine_id,
                instrument_code,
                instrument_name,
                frequency
            )
        )

        self.db.conn.commit()

    # =========================================================
    # Update Instrument
    # =========================================================

    def update_instrument(
        self,
        old_instrument_code,
        machine_code,
        machine_name,
        department,
        instrument_code,
        instrument_name,
        frequency
    ):
        cursor = self.db.cursor

        cursor.execute(
            """
            SELECT
                i.id,
                i.machine_id
            FROM instruments i
            WHERE i.instrument_code=?
            """,
            (old_instrument_code,)
        )

        instrument = cursor.fetchone()

        if not instrument:
            raise Exception("Instrument not found.")

        instrument_id, current_machine_id = instrument

        if instrument_code != old_instrument_code:
            cursor.execute(
                """
                SELECT id
                FROM instruments
                WHERE instrument_code=?
                """,
                (instrument_code,)
            )
            if cursor.fetchone():
                raise Exception("Instrument Code already exists.")

        cursor.execute(
            """
            SELECT id
            FROM machines
            WHERE machine_code=?
            """,
            (machine_code,)
        )

        machine = cursor.fetchone()

        if machine and machine[0] != current_machine_id:
            raise Exception("Machine Code already exists.")

        if machine:
            target_machine_id = machine[0]
            cursor.execute(
                """
                UPDATE machines
                SET machine_name=?, department=?
                WHERE id=?
                """,
                (machine_name, department, target_machine_id)
            )
        else:
            cursor.execute(
                """
                UPDATE machines
                SET machine_code=?, machine_name=?, department=?
                WHERE id=?
                """,
                (machine_code, machine_name, department, current_machine_id)
            )
            target_machine_id = current_machine_id

        cursor.execute(
            """
            UPDATE instruments
            SET machine_id=?, instrument_code=?, instrument_name=?, frequency=?
            WHERE id=?
            """,
            (
                target_machine_id,
                instrument_code,
                instrument_name,
                frequency,
                instrument_id,
            )
        )

        self.db.conn.commit()

    # =========================================================

    def close(self):
        self.db.close()