from database.db_manager import Database


class InstrumentService:

    def __init__(self):
        self.db = Database()

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

    # -----------------------------------------------------

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

        # Check machine

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

        # Check Instrument

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

    def close(self):

        self.db.close()