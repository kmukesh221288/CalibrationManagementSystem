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

        cursor = self.db.cursor()

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

    def close(self):

        self.db.close()