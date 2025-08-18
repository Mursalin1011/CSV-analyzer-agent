import sqlite3
import os

# Database file path
DATABASE_FILE = "insights_cache.db"

def clear_database():
    """Clear all records from the insights_cache table"""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        
        # Delete all records from the table
        cursor.execute('DELETE FROM insights_cache')
        
        conn.commit()
        conn.close()
        print("Successfully cleared all records from the insights_cache table")
    except Exception as e:
        print(f"Error clearing database: {e}")

if __name__ == "__main__":
    clear_database()