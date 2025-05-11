import json
import os
import sqlite3
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from crewai.memory.storage.interface import Storage
from pydantic import BaseModel, Field


class ProjectMemoryStorage(Storage):
    """Storage for project memory items.
    
    This class implements the Storage interface for project memory items.
    """
    
    def __init__(
        self,
        project_name: str,
        project_code: Optional[str] = None,
        db_path: Optional[str] = None,
    ):
        """Initialize the project memory storage.
        
        Args:
            project_name: The name of the project.
            project_code: The project code.
            db_path: The path to the SQLite database file.
        """
        self.project_name = project_name
        self.project_code = project_code
        
        # Determine the database path
        if db_path is None:
            # Use a default path in the user's home directory
            home_dir = os.path.expanduser("~")
            pmoai_dir = os.path.join(home_dir, ".pmoai", "memory")
            os.makedirs(pmoai_dir, exist_ok=True)
            
            # Create a filename based on the project name and code
            filename = f"{project_name.lower().replace(' ', '_')}"
            if project_code:
                filename += f"_{project_code.lower().replace(' ', '_')}"
            filename += ".db"
            
            db_path = os.path.join(pmoai_dir, filename)
        
        self.db_path = db_path
        
        # Initialize the database
        self._init_db()
    
    def _init_db(self) -> None:
        """Initialize the database schema."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create the project_memories table if it doesn't exist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS project_memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_name TEXT NOT NULL,
            project_code TEXT,
            memory_type TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            author TEXT,
            tags TEXT,
            metadata TEXT
        )
        """)
        
        conn.commit()
        conn.close()
    
    def save(self, item: Any, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Save a memory item to the storage.
        
        Args:
            item: The memory item to save.
            metadata: Additional metadata (not used, as metadata is included in the item).
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Convert tags to JSON string
        tags_json = json.dumps(item.tags)
        
        # Convert metadata to JSON string
        metadata_json = json.dumps(item.metadata)
        
        # Insert the memory item
        cursor.execute(
            """
            INSERT INTO project_memories
            (project_name, project_code, memory_type, content, timestamp, author, tags, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                item.project_name,
                item.project_code,
                item.memory_type,
                item.content,
                item.timestamp,
                item.author,
                tags_json,
                metadata_json,
            ),
        )
        
        conn.commit()
        conn.close()
    
    def search(
        self,
        query: str,
        memory_type: Optional[str] = None,
        limit: int = 5,
        score_threshold: float = 0.35,
    ) -> List[Any]:
        """Search for memory items in the storage.
        
        Args:
            query: The search query.
            memory_type: The type of memory to search for.
            limit: The maximum number of results to return.
            score_threshold: The minimum similarity score for results (not used in this implementation).
            
        Returns:
            A list of matching memory items.
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Build the SQL query
        sql = """
        SELECT * FROM project_memories
        WHERE project_name = ?
        """
        params = [self.project_name]
        
        if self.project_code:
            sql += " AND project_code = ?"
            params.append(self.project_code)
        
        if memory_type:
            sql += " AND memory_type = ?"
            params.append(memory_type)
        
        # Add a simple text search condition
        sql += " AND content LIKE ?"
        params.append(f"%{query}%")
        
        # Order by timestamp (most recent first) and limit results
        sql += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)
        
        # Execute the query
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        
        # Convert rows to memory items
        from pmoai.memory.project_memory import ProjectMemoryItem
        
        items = []
        for row in rows:
            items.append(
                ProjectMemoryItem(
                    project_name=row["project_name"],
                    project_code=row["project_code"],
                    memory_type=row["memory_type"],
                    content=row["content"],
                    timestamp=row["timestamp"],
                    author=row["author"],
                    tags=json.loads(row["tags"]),
                    metadata=json.loads(row["metadata"]),
                )
            )
        
        conn.close()
        return items
