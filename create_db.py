import sqlite3
import os

# Path to the database file
db_path = 'instance/my_database.db'

# Ensure the directory exists
os.makedirs(os.path.dirname(db_path), exist_ok=True)

# Create the database file
conn = sqlite3.connect(db_path)
conn.close()

print(f"Database created at {db_path}")
