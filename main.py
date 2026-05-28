# main.py

from core.logging_manager import LoggingManager
from database.db_manager import DatabaseManager

LoggingManager.initialize()

db = DatabaseManager()
db.connect()
db.initialize_schema()

print("System initialized successfully.")