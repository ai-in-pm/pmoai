"""
Minimal example to test PMOAI functionality.
"""

import os
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

# Import directly from crewai to test if it works
try:
    from crewai import Agent as CrewAIAgent
    from crewai import Task as CrewAITask
    from crewai import Crew as CrewAICrew
    
    print("Successfully imported CrewAI components")
    
    # Create a simple agent using CrewAI directly
    agent = CrewAIAgent(
        role="Test Agent",
        goal="Test the CrewAI installation",
        backstory="I am a test agent created to verify the CrewAI installation."
    )
    print("Successfully created a CrewAI agent")
    
    # Create a simple task
    task = CrewAITask(
        description="Test task",
        expected_output="Test output",
        agent=agent
    )
    print("Successfully created a CrewAI task")
    
    # Create a simple crew
    crew = CrewAICrew(
        agents=[agent],
        tasks=[task],
        verbose=True
    )
    print("Successfully created a CrewAI crew")
    
    print("CrewAI test completed successfully!")
except Exception as e:
    print(f"Error with CrewAI: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*50 + "\n")

# Now try to use some basic PMOAI functionality that doesn't depend on problematic imports
try:
    # Import utilities that are less likely to have dependency issues
    from pmoai.utilities import I18N
    print("Successfully imported PMOAI utilities")
    
    # Try to use the I18N utility
    i18n = I18N()
    print(f"Default language: {i18n.language}")
    
    print("PMOAI utilities test completed successfully!")
except Exception as e:
    print(f"Error with PMOAI utilities: {e}")
    import traceback
    traceback.print_exc()
