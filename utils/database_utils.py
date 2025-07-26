import sqlite3
from typing import List, Dict, Any

class QuizDatabase:
    """
    Simple utility class for interacting with the quiz SQLite database
    """
    
    def __init__(self, db_path: str = "data/quiz_database.db"):
        self.db_path = db_path
    
    def get_connection(self) -> sqlite3.Connection:
        """Get a database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable dict-like access to rows
        return conn
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """
        Execute a query and return results as list of dictionaries
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

# Initialize default database instance
quiz_db = QuizDatabase()
