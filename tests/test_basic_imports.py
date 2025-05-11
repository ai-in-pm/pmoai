"""
Simple test script to verify basic PMOAI imports.
"""

import os
import sys

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

try:
    # Import the main package
    import pmoai
    print(f"Successfully imported pmoai package")
    print(f"PMOAI version: {pmoai.__version__}")
    
    # Import basic components without dependencies on agent adapters
    from pmoai.crew import Crew
    print("Successfully imported Crew")
    
    from pmoai.task import Task
    print("Successfully imported Task")
    
    # Try to import Agent without the problematic imports
    from pmoai.agent import Agent
    print("Successfully imported Agent")
    
    print("Basic imports test completed successfully!")
except Exception as e:
    print(f"Error: {e}")
    print(f"Error type: {type(e)}")
    import traceback
    traceback.print_exc()
