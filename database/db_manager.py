import sqlite3
from pathlib import Path


DB_FILE = Path(__file__).parent / "calibration.db"


class Database:

    def __init__(self):

        self.conn = sqlite3.connect(DB_FILE)

        self.conn.execute("PRAGMA foreign_keys = ON")

        self.cursor = self.conn.cursor()

    def create_tables(self):

        # ===========================
        # MACHINES
        # ===========================

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS machines(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            machine_code TEXT UNIQUE,

            machine_name TEXT NOT NULL,

            department TEXT,

            location TEXT,

            manufacturer TEXT,

            model TEXT,

            serial_number TEXT,

            status TEXT DEFAULT 'Active'

        )
        """)

        # ===========================
        # INSTRUMENTS
        # ===========================

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS instruments(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            machine_id INTEGER,

            instrument_code TEXT UNIQUE,

            instrument_name TEXT,

            accuracy TEXT,

            least_count TEXT,

            master_instrument TEXT,

            frequency TEXT,

            calibration_agency TEXT,

            active INTEGER DEFAULT 1,

            FOREIGN KEY(machine_id)
            REFERENCES machines(id)

        )
        """)

        # ===========================
        # CALIBRATION HISTORY
        # ===========================

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS calibration_history(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            instrument_id INTEGER NOT NULL,

            calibration_date TEXT NOT NULL,

            next_due_date TEXT NOT NULL,

            calibration_type TEXT NOT NULL,

            agency TEXT,

            certificate_number TEXT,

            cost REAL,

            result TEXT,

            remarks TEXT,

            certificate_path TEXT,

            created_on TEXT,

            FOREIGN KEY(instrument_id)
            REFERENCES instruments(id)

        )
        """)

        # ===========================
        # SETTINGS
        # ===========================

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings(

            id INTEGER PRIMARY KEY,

            company_name TEXT,

            reminder_days INTEGER,

            theme TEXT

        )
        """)

        self.conn.commit()

    def close(self):

        self.conn.close()