"""
Test script to verify that we can import pmoai utilities.
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

# Try to import pmoai utilities directly
try:
    # Import utilities
    from pmoai.utilities import I18N, paths
    print("Successfully imported pmoai.utilities")
    
    # Try to use the I18N utility
    i18n = I18N()
    print(f"Default language: {i18n.language}")
    
    # Try to use the paths utility
    print(f"DB storage path: {paths.db_storage_path()}")
    
    print("PMOAI utilities test completed successfully!")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
