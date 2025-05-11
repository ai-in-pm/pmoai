"""Example of using the memory module in PMOAI."""

from pmoai.memory import (
    ContextualMemory,
    EntityMemory,
    EntityMemoryItem,
    ExternalMemory,
    LongTermMemory,
    LongTermMemoryItem,
    ShortTermMemory,
    UserMemory,
)


def main():
    """Run the memory example."""
    # Initialize memory components
    stm = ShortTermMemory()
    ltm = LongTermMemory()
    em = EntityMemory()
    um = UserMemory()
    exm = ExternalMemory()
    
    # Create a contextual memory
    cm = ContextualMemory(
        memory_config=None,
        stm=stm,
        ltm=ltm,
        em=em,
        um=um,
        exm=exm,
    )
    
    # Save short-term memories
    stm.save(
        value="The project timeline has been updated to include a new milestone for user testing.",
        metadata={"type": "project_update", "importance": "high"},
        agent="Project Manager",
    )
    
    stm.save(
        value="The development team has completed the backend API implementation ahead of schedule.",
        metadata={"type": "development_update", "importance": "medium"},
        agent="Lead Developer",
    )
    
    # Save entity memories
    em.save(
        EntityMemoryItem(
            name="John Smith",
            type="Stakeholder",
            description="CEO of client company, main decision maker for the project",
            relationships="Reports to the board, manages Sarah Johnson",
        )
    )
    
    em.save(
        EntityMemoryItem(
            name="Project X",
            type="Project",
            description="A new project management system with AI capabilities",
            relationships="Owned by John Smith, developed by our team",
        )
    )
    
    # Save long-term memory
    ltm.save(
        LongTermMemoryItem(
            agent="Project Manager",
            task="Create project schedule",
            expected_output="Detailed project schedule with milestones",
            datetime="2023-06-15T14:30:00",
            quality=0.9,
            metadata={
                "quality": 0.9,
                "suggestions": [
                    "Include more buffer time for testing phases",
                    "Add explicit handoff points between teams",
                    "Schedule regular stakeholder review meetings",
                ],
            },
        )
    )
    
    # Search for relevant information
    query = "project timeline updates"
    
    print(f"Query: {query}")
    print("\nShort-term Memory Results:")
    stm_results = stm.search(query)
    for result in stm_results:
        print(f"- {result.get('context', '')} (Score: {result.get('score', 0):.2f})")
    
    print("\nEntity Memory Results:")
    em_results = em.search(query)
    for result in em_results:
        print(f"- {result.get('context', '')} (Score: {result.get('score', 0):.2f})")
    
    # Build context for a task
    task_description = "Update the project schedule based on recent progress"
    context = "We need to adjust the timeline for the next phase"
    
    class MockTask:
        def __init__(self, description):
            self.description = description
    
    task = MockTask(task_description)
    
    print("\nContextual Memory for Task:")
    context_result = cm.build_context_for_task(task, context)
    print(context_result)


if __name__ == "__main__":
    main()
