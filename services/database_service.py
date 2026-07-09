import os
import shutil
import sqlite3
from datetime import datetime
from pathlib import Path


class DatabaseService:
    def __init__(self, db_path=None, backup_dir=None):
        base_dir = Path(__file__).resolve().parent.parent
        self.db_path = Path(db_path) if db_path else base_dir / "database" / "calibration.db"
        self.backup_dir = Path(backup_dir) if backup_dir else base_dir / "backups"

    def backup_database(self):
        os.makedirs(self.backup_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = self.backup_dir / f"Calibration_Backup_{timestamp}.db"
        shutil.copy2(self.db_path, backup_file)

        return str(backup_file.resolve())

    def restore_database(self, backup_file):
        backup_path = Path(backup_file)

        if not backup_path.exists() or not backup_path.is_file():
            raise FileNotFoundError("Backup file does not exist or is not a valid file.")

        self._validate_backup_file(backup_path)

        os.makedirs(self.db_path.parent, exist_ok=True)
        shutil.copy2(backup_path, self.db_path)
        return True

    def _validate_backup_file(self, backup_path):
        try:
            connection = sqlite3.connect(backup_path)
            connection.execute("SELECT name FROM sqlite_master LIMIT 1")
            connection.close()
        except sqlite3.DatabaseError as exc:
            raise ValueError("Backup file is invalid.") from exc
