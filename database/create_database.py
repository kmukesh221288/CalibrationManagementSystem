from database.db_manager import Database

db = Database()

db.create_tables()

db.close()

print("Database Created Successfully")