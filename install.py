import os
import subprocess
import sys

def main():
    print("=== Installing PMOAI ===")
    
    # Check if pip is available
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "--version"])
    except subprocess.CalledProcessError:
        print("Error: pip is not available. Please install pip first.")
        sys.exit(1)
    
    # Install PMOAI in development mode
    try:
        print("\nInstalling PMOAI...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-e", "."])
        print("PMOAI installed successfully!")
    except subprocess.CalledProcessError:
        print("Error: Failed to install PMOAI.")
        sys.exit(1)
    
    # Verify installation
    try:
        print("\nVerifying installation...")
        subprocess.check_call([sys.executable, "examples/verify_installation.py"])
    except subprocess.CalledProcessError:
        print("Error: Failed to verify PMOAI installation.")
        sys.exit(1)
    
    print("\n=== Installation Complete ===")
    print("You can now use PMOAI in your projects.")
    print("Remember to set your OpenAI API key as an environment variable:")
    print("  export OPENAI_API_KEY=your-api-key  # Linux/Mac")
    print("  set OPENAI_API_KEY=your-api-key     # Windows")


if __name__ == "__main__":
    main()
