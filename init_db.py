import os
from utils.db import init_db

# Initialize database tables
if __name__ == "__main__":
    try:
        engine = init_db()
        print("Database initialized successfully!")
        print(f"Connected to: {engine.url}")
    except Exception as e:
        print(f"Error initializing database: {e}")