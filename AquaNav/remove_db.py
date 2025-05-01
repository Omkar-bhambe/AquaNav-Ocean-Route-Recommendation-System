import os

db_path = "Aquanav.db"  # or the full path if it's different

if os.path.exists(db_path):
    os.remove(db_path)
    print("Corrupted database.db deleted.")
else:
    print("database.db not found.")
