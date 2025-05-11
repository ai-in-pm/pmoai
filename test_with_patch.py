"""
Test script to verify that we can import pmoai modules with the TensorFlow patch.
"""

import os
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

# Apply the TensorFlow patch
print("Applying TensorFlow patch...")
exec(open("patch_tensorflow.py").read())

# Apply the agents patch
print("\nApplying agents patch...")
exec(open("patch_agents.py").read())

# Try to import pmoai modules directly
try:
    # Import the package
    import pmoai
    print(f"Successfully imported pmoai package")
    print(f"PMOAI version: {pmoai.__version__}")

    # Import utilities
    from pmoai.utilities.paths import db_storage_path
    print(f"DB storage path: {db_storage_path()}")

    # Import knowledge components
    from pmoai.knowledge.embedder.base_embedder import BaseEmbedder
    print("Successfully imported BaseEmbedder")

    # Import memory components
    from pmoai.memory.storage.base_memory_storage import BaseMemoryStorage
    print("Successfully imported BaseMemoryStorage")

    # Import tools components
    from pmoai.tools.base_tool import BaseTool
    print("Successfully imported BaseTool")

    print("Basic imports test completed successfully!")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
