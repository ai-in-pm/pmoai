"""Storage for kickoff task outputs."""

import json
import os
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


class KickoffTaskOutputsSQLiteStorage:
    """Storage for kickoff task outputs using SQLite."""
    
    def __init__(self, db_path: Optional[str] = None):
        """Initialize the storage.
        
        Args:
            db_path: The path to the SQLite database file.
        """
        # Determine the database path
        if db_path is None:
            # Use a default path in the user's home directory
            home_dir = os.path.expanduser("~")
            pmoai_dir = os.path.join(home_dir, ".pmoai", "memory")
            os.makedirs(pmoai_dir, exist_ok=True)
            db_path = os.path.join(pmoai_dir, "kickoff_task_outputs.db")
        
        self.db_path = db_path
        
        # Initialize the database
        self._init_db()
    
    def _init_db(self) -> None:
        """Initialize the database schema."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create the kickoff_task_outputs table if it doesn't exist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS kickoff_task_outputs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id TEXT NOT NULL,
            expected_output TEXT NOT NULL,
            raw TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
        """)
        
        conn.commit()
        conn.close()
    
    def save(self, task_outputs: List[Dict[str, Any]]) -> None:
        """Save task outputs to the storage.
        
        Args:
            task_outputs: The task outputs to save.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Clear existing task outputs
        cursor.execute("DELETE FROM kickoff_task_outputs")
        
        # Insert new task outputs
        for task_output in task_outputs:
            cursor.execute(
                """
                INSERT INTO kickoff_task_outputs
                (task_id, expected_output, raw, timestamp)
                VALUES (?, ?, ?, ?)
                """,
                (
                    task_output["task_id"],
                    task_output["expected_output"],
                    task_output["raw"],
                    datetime.now().isoformat(),
                ),
            )
        
        conn.commit()
        conn.close()
    
    def load(self) -> List[Dict[str, Any]]:
        """Load task outputs from the storage.
        
        Returns:
            The task outputs.
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Query task outputs
        cursor.execute(
            """
            SELECT task_id, expected_output, raw, timestamp
            FROM kickoff_task_outputs
            ORDER BY id
            """
        )
        
        rows = cursor.fetchall()
        
        # Convert rows to dictionaries
        task_outputs = []
        for row in rows:
            task_outputs.append(dict(row))
        
        conn.close()
        
        return task_outputs
    
    def clear(self) -> None:
        """Clear all task outputs from the storage."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Clear existing task outputs
        cursor.execute("DELETE FROM kickoff_task_outputs")
        
        conn.commit()
        conn.close()
