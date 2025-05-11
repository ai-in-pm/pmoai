"""
Utility script to set the OpenAI API key in the .env file and as an environment variable.
"""

import os
import sys

def set_api_key():
    """Set the OpenAI API key in the .env file and as an environment variable."""
    print("OpenAI API Key Setup Utility")
    print("============================")
    print("This utility will help you set up your OpenAI API key for use with PMOAI.")
    print("Your API key should look like: sk-abcdefghijklmnopqrstuvwxyz123456789")
    print()
    
    # Get the API key from the user
    api_key = input("Enter your OpenAI API key: ")
    
    # Clean the API key
    if "set " in api_key.lower():
        api_key = api_key.lower().replace("set ", "")
    if "openai_api_key=" in api_key.lower():
        api_key = api_key.lower().replace("openai_api_key=", "")
    # Remove quotes if present
    api_key = api_key.strip('"\'')
    
    # Validate the API key format (basic check)
    if not api_key.startswith("sk-"):
        print("Warning: Your API key doesn't start with 'sk-'. This may not be a valid OpenAI API key.")
        confirm = input("Continue anyway? (y/n): ")
        if confirm.lower() != 'y':
            print("Operation cancelled.")
            return
    
    # Set the API key in the environment
    os.environ["OPENAI_API_KEY"] = api_key
    print("API key set in the current process environment.")
    
    # Find the .env file
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_file_path = os.path.join(root_dir, ".env")
    
    # Update the .env file
    try:
        # Read the current content
        if os.path.exists(env_file_path):
            with open(env_file_path, "r") as f:
                lines = f.readlines()
            
            # Find and replace the OPENAI_API_KEY line
            key_found = False
            for i, line in enumerate(lines):
                if line.strip().startswith("OPENAI_API_KEY="):
                    lines[i] = f"OPENAI_API_KEY={api_key}\n"
                    key_found = True
                    break
            
            # If the key wasn't found, add it
            if not key_found:
                lines.append(f"OPENAI_API_KEY={api_key}\n")
            
            # Write the updated content
            with open(env_file_path, "w") as f:
                f.writelines(lines)
        else:
            # Create a new .env file
            with open(env_file_path, "w") as f:
                f.write(f"OPENAI_API_KEY={api_key}\n")
        
        print(f"API key saved to {env_file_path}")
    except Exception as e:
        print(f"Error updating .env file: {e}")
    
    # Create a batch file to set the API key for future terminal sessions
    batch_file_path = os.path.join(os.path.dirname(__file__), "set_openai_key.bat")
    with open(batch_file_path, "w") as f:
        f.write(f"@echo off\n")
        f.write(f"set OPENAI_API_KEY={api_key}\n")
        f.write(f"echo OpenAI API key set successfully!\n")
    
    print(f"Created batch file: {batch_file_path}")
    print("To set the API key in a new terminal session, run:")
    print(f"  {batch_file_path}")
    
    print("\nSetup complete! You can now run PMOAI scripts that require an OpenAI API key.")

if __name__ == "__main__":
    set_api_key()
