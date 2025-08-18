import sqlite3
import os
from typing import Optional, List, Tuple
from csv_analyzer.core.config import Config

class CacheManager:
    """Manages caching of insights in SQLite database"""
    
    def __init__(self, db_file: str = Config.DATABASE_FILE):
        self.db_file = db_file
        self.init_db()
    
    def init_db(self):
        """Initialize the SQLite database with the required table"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Create table for storing insights
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS insights_cache (
                cache_key TEXT PRIMARY KEY,
                insights TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_insights(self, cache_key: str, insights: str) -> bool:
        """Save insights to SQLite database"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Insert or replace the insights
            cursor.execute('''
                INSERT OR REPLACE INTO insights_cache (cache_key, insights)
                VALUES (?, ?)
            ''', (cache_key, insights))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error saving to database: {e}")
            return False
    
    def load_insights(self, cache_key: str) -> Optional[str]:
        """Load insights from SQLite database"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT insights FROM insights_cache WHERE cache_key = ?
            ''', (cache_key,))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return result[0]
            return None
        except Exception as e:
            print(f"Error loading from database: {e}")
            return None
    
    def get_all_insights(self) -> List[Tuple[str, str]]:
        """Get all insights from SQLite database"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT cache_key, insights FROM insights_cache
            ''')
            
            results = cursor.fetchall()
            conn.close()
            
            return results
        except Exception as e:
            print(f"Error loading all insights from database: {e}")
            return []