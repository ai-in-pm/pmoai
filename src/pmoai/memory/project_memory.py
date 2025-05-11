from typing import Any, Dict, List, Optional

from crewai.memory.memory import Memory
from pydantic import BaseModel, Field

from pmoai.memory.storage.project_memory_storage import ProjectMemoryStorage


class ProjectMemoryItem(BaseModel):
    """Represents a project memory item."""
    
    project_name: str = Field(description="The name of the project.")
    project_code: Optional[str] = Field(None, description="The project code.")
    memory_type: str = Field(description="The type of memory (e.g., 'decision', 'issue', 'lesson').")
    content: str = Field(description="The content of the memory.")
    timestamp: str = Field(description="The timestamp of the memory.")
    author: Optional[str] = Field(None, description="The author of the memory.")
    tags: List[str] = Field(default_factory=list, description="Tags associated with the memory.")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata.")


class ProjectMemory(Memory):
    """Memory for project-specific information.
    
    This class extends the Memory class to provide project-specific memory capabilities.
    """
    
    def __init__(
        self,
        project_name: str,
        project_code: Optional[str] = None,
        storage: Optional[ProjectMemoryStorage] = None,
        **kwargs: Any,
    ):
        """Initialize the project memory.
        
        Args:
            project_name: The name of the project.
            project_code: The project code.
            storage: The storage to use for the memory.
            **kwargs: Additional arguments to pass to the parent constructor.
        """
        storage = storage or ProjectMemoryStorage(
            project_name=project_name,
            project_code=project_code,
        )
        super().__init__(storage=storage, **kwargs)
        self.project_name = project_name
        self.project_code = project_code
    
    def add_decision(
        self,
        decision: str,
        author: Optional[str] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Add a decision to the project memory.
        
        Args:
            decision: The decision to add.
            author: The author of the decision.
            tags: Tags associated with the decision.
            metadata: Additional metadata.
        """
        item = ProjectMemoryItem(
            project_name=self.project_name,
            project_code=self.project_code,
            memory_type="decision",
            content=decision,
            timestamp=self._get_current_timestamp(),
            author=author,
            tags=tags or [],
            metadata=metadata or {},
        )
        self.storage.save(item)
    
    def add_issue(
        self,
        issue: str,
        author: Optional[str] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Add an issue to the project memory.
        
        Args:
            issue: The issue to add.
            author: The author of the issue.
            tags: Tags associated with the issue.
            metadata: Additional metadata.
        """
        item = ProjectMemoryItem(
            project_name=self.project_name,
            project_code=self.project_code,
            memory_type="issue",
            content=issue,
            timestamp=self._get_current_timestamp(),
            author=author,
            tags=tags or [],
            metadata=metadata or {},
        )
        self.storage.save(item)
    
    def add_lesson(
        self,
        lesson: str,
        author: Optional[str] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Add a lesson learned to the project memory.
        
        Args:
            lesson: The lesson to add.
            author: The author of the lesson.
            tags: Tags associated with the lesson.
            metadata: Additional metadata.
        """
        item = ProjectMemoryItem(
            project_name=self.project_name,
            project_code=self.project_code,
            memory_type="lesson",
            content=lesson,
            timestamp=self._get_current_timestamp(),
            author=author,
            tags=tags or [],
            metadata=metadata or {},
        )
        self.storage.save(item)
    
    def search_decisions(
        self, query: str, limit: int = 5, score_threshold: float = 0.35
    ) -> List[ProjectMemoryItem]:
        """Search for decisions in the project memory.
        
        Args:
            query: The search query.
            limit: The maximum number of results to return.
            score_threshold: The minimum similarity score for results.
            
        Returns:
            A list of matching decisions.
        """
        return self.storage.search(
            query=query,
            memory_type="decision",
            limit=limit,
            score_threshold=score_threshold,
        )
    
    def search_issues(
        self, query: str, limit: int = 5, score_threshold: float = 0.35
    ) -> List[ProjectMemoryItem]:
        """Search for issues in the project memory.
        
        Args:
            query: The search query.
            limit: The maximum number of results to return.
            score_threshold: The minimum similarity score for results.
            
        Returns:
            A list of matching issues.
        """
        return self.storage.search(
            query=query,
            memory_type="issue",
            limit=limit,
            score_threshold=score_threshold,
        )
    
    def search_lessons(
        self, query: str, limit: int = 5, score_threshold: float = 0.35
    ) -> List[ProjectMemoryItem]:
        """Search for lessons in the project memory.
        
        Args:
            query: The search query.
            limit: The maximum number of results to return.
            score_threshold: The minimum similarity score for results.
            
        Returns:
            A list of matching lessons.
        """
        return self.storage.search(
            query=query,
            memory_type="lesson",
            limit=limit,
            score_threshold=score_threshold,
        )
    
    def _get_current_timestamp(self) -> str:
        """Get the current timestamp in ISO format.
        
        Returns:
            The current timestamp.
        """
        from datetime import datetime
        return datetime.now().isoformat()
