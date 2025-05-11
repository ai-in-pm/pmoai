from typing import Any, Dict, List

from pmoai.memory.long_term.long_term_memory_item import LongTermMemoryItem
from pmoai.memory.memory import Memory
from pmoai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage


class LongTermMemory(Memory):
    """
    LongTermMemory class for managing cross runs data related to overall crew's
    execution and performance.
    Inherits from the Memory class and utilizes an instance of a class that
    adheres to the Storage for data storage, specifically working with
    LongTermMemoryItem instances.
    """

    def __init__(self, storage=None, path=None):
        if not storage:
            storage = LTMSQLiteStorage(db_path=path) if path else LTMSQLiteStorage()
        super().__init__(storage=storage)

    def save(self, item: LongTermMemoryItem) -> None:
        metadata = item.metadata
        metadata.update({"agent": item.agent, "expected_output": item.expected_output})
        self.storage.save(
            task_description=item.task,
            score=metadata["quality"],
            metadata=metadata,
            datetime=item.datetime,
        )

    def search(self, task: str, latest_n: int = 3) -> List[Dict[str, Any]]:
        return self.storage.load(task, latest_n)

    def reset(self) -> None:
        self.storage.reset()
