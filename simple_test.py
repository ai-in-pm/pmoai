"""
Simple test script to verify PMOAI installation.
"""

import os
import sys

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

print("PMOAI Installation Test")
print("======================")
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print(f"Working directory: {os.getcwd()}")
print(f"Source directory: {os.path.join(os.path.dirname(__file__), 'src')}")
print("======================")

# Try to import the package without importing problematic modules
try:
    sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
    from pmoai import __version__
    print(f"PMOAI version: {__version__}")
    print("PMOAI package imported successfully!")
except Exception as e:
    print(f"Error importing pmoai package: {e}")

print("======================")
print("Installed packages:")
import pkg_resources
for package in pkg_resources.working_set:
    print(f"  {package.project_name} {package.version}")

print("======================")
print("Test completed!")
