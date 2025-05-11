"""
Simple test script to verify PMOAI installation.
"""

import os
import sys

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

try:
    import pmoai
    print(f"PMOAI version: {pmoai.__version__}")
    
    # Import basic components
    from pmoai import Agent, Task, Crew
    print("Successfully imported Agent, Task, and Crew")
    
    # Create a simple agent
    agent = Agent(
        role="Test Agent",
        goal="Test the PMOAI installation",
        backstory="I am a test agent created to verify the PMOAI installation."
    )
    print("Successfully created an agent")
    
    # Create a simple task
    task = Task(
        description="Test task",
        expected_output="Test output",
        agent=agent
    )
    print("Successfully created a task")
    
    print("PMOAI installation test completed successfully!")
except Exception as e:
    print(f"Error: {e}")
    print(f"Error type: {type(e)}")
    print(f"Error traceback: {sys.exc_info()[2]}")
