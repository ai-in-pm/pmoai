"""Example of using the knowledge module in PMOAI."""

from pmoai.knowledge import (
    CrewDoclingSource,
    Knowledge,
    PMMethodologyKnowledgeSource,
    StringKnowledgeSource,
)


def main():
    """Run the knowledge example."""
    # Create a knowledge base
    knowledge = Knowledge(
        collection_name="project_knowledge",
        sources=[
            # Add a string knowledge source
            StringKnowledgeSource(
                content="""
                # Project Requirements
                
                The project requires the development of a new project management system
                with the following features:
                
                1. Task management
                2. Resource allocation
                3. Gantt chart visualization
                4. Risk management
                5. Budget tracking
                
                The system should be web-based and accessible from mobile devices.
                """
            ),
            
            # Add a PM methodology knowledge source
            PMMethodologyKnowledgeSource(methodology="agile"),
            
            # Add a crew docling source
            CrewDoclingSource(
                crew_name="Project Management Team",
                crew_description="A team of project management experts working on the new PM system.",
                agents=[
                    {
                        "name": "Project Manager",
                        "role": "Lead the project and coordinate the team",
                        "goal": "Ensure the project is completed on time and within budget",
                    },
                    {
                        "name": "Business Analyst",
                        "role": "Gather and analyze requirements",
                        "goal": "Ensure the system meets user needs",
                    },
                    {
                        "name": "Developer",
                        "role": "Implement the system",
                        "goal": "Create a high-quality, maintainable codebase",
                    },
                ],
                tasks=[
                    {
                        "name": "Requirements Gathering",
                        "description": "Gather and document requirements from stakeholders",
                        "expected_output": "Requirements document",
                        "agent": "Business Analyst",
                    },
                    {
                        "name": "System Design",
                        "description": "Design the system architecture",
                        "expected_output": "System design document",
                        "agent": "Developer",
                        "dependencies": ["Requirements Gathering"],
                    },
                ],
                project_info={
                    "name": "PM System",
                    "start_date": "2023-01-01",
                    "end_date": "2023-06-30",
                    "budget": "$500,000",
                },
            ),
        ],
    )
    
    # Add the sources to the knowledge base
    knowledge.add_sources()
    
    # Query the knowledge base
    results = knowledge.query(
        query=["What methodology should we use for this project?"],
        results_limit=3,
        score_threshold=0.35,
    )
    
    # Print the results
    print("Query: What methodology should we use for this project?")
    print("Results:")
    for i, result in enumerate(results, 1):
        print(f"\nResult {i} (Score: {result['score']:.2f}):")
        print(f"Context: {result['text'][:200]}...")


if __name__ == "__main__":
    main()
