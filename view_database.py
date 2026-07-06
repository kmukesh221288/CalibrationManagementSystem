import sqlite3
from pathlib import Path

DB_FILE = Path("database") / "calibration.db"

conn = sqlite3.connect(DB_FILE)

cursor = conn.cursor()

print("=" * 60)
print("MACHINES")
print("=" * 60)

cursor.execute("""
SELECT id,
       machine_code,
       machine_name,
       department
FROM machines
ORDER BY machine_name
""")

machines = cursor.fetchall()

print(f"\nTotal Machines : {len(machines)}\n")

for machine in machines:

    print(machine)

print("\n")

print("=" * 60)
print("INSTRUMENTS")
print("=" * 60)

cursor.execute("""
SELECT id,
       instrument_code,
       instrument_name,
       frequency
FROM instruments
ORDER BY instrument_name
""")

instruments = cursor.fetchall()

print(f"\nTotal Instruments : {len(instruments)}\n")

for instrument in instruments:

    print(instrument)

print("\n")

print("=" * 60)
print("CALIBRATION HISTORY")
print("=" * 60)

cursor.execute("""
SELECT id,
       instrument_id,
       calibration_date,
       next_due_date
FROM calibration_history
ORDER BY id DESC
LIMIT 20
""")

history = cursor.fetchall()

print(f"\nShowing Last {len(history)} Records\n")

for row in history:

    print(row)

conn.close()