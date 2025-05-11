"""
Script to set the OpenAI API key in the environment.
Run this script before running the example scripts.
"""

import os
import sys
import subprocess

def set_api_key():
    print("=" * 50)
    print("OPENAI API KEY SETUP")
    print("=" * 50)
    
    # Check if API key is already set
    if "OPENAI_API_KEY" in os.environ and os.environ["OPENAI_API_KEY"]:
        print(f"API key is already set in the environment.")
        change_key = input("Do you want to change it? (y/n): ")
        if change_key.lower() != 'y':
            print("Keeping the existing API key.")
            return
    
    # Get the API key from the user
    api_key = input("Enter your OpenAI API key: ")
    if not api_key:
        print("No API key provided. Exiting.")
        return
    
    # Set the API key in the environment
    os.environ["OPENAI_API_KEY"] = api_key
    print("API key set in the current process environment.")
    
    # Create a batch file to set the API key for future terminal sessions
    batch_file_path = os.path.join(os.path.dirname(__file__), "set_openai_key.bat")
    with open(batch_file_path, "w") as f:
        f.write(f"@echo off\n")
        f.write(f"set OPENAI_API_KEY={api_key}\n")
        f.write(f"echo OpenAI API key set successfully!\n")
    
    print(f"Created batch file: {batch_file_path}")
    print("To set the API key in a new terminal session, run:")
    print(f"  {batch_file_path}")
    
    # Ask if the user wants to run an example script
    run_example = input("Do you want to run an example script now? (y/n): ")
    if run_example.lower() == 'y':
        print("\nAvailable example scripts:")
        print("1. use_crewai_simple.py - A simple example")
        print("2. pmo_example.py - A more comprehensive PMO example")
        choice = input("Enter your choice (1 or 2): ")
        
        if choice == '1':
            print("\nRunning use_crewai_simple.py...")
            subprocess.run([sys.executable, "use_crewai_simple.py"])
        elif choice == '2':
            print("\nRunning pmo_example.py...")
            subprocess.run([sys.executable, "pmo_example.py"])
        else:
            print("Invalid choice. Please run the scripts manually.")
    
    print("\nSetup complete!")

if __name__ == "__main__":
    set_api_key()
