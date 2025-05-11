#!/bin/bash
# Example script demonstrating PMOAI CLI usage

# List available agents
echo "Listing available agents..."
pmoai list agents

# List available tasks
echo -e "\nListing available tasks..."
pmoai list tasks

# List available crews
echo -e "\nListing available crews..."
pmoai list crews

# Initialize configuration files in a custom directory
echo -e "\nInitializing configuration files in 'custom_config' directory..."
mkdir -p custom_config
pmoai init --output-dir custom_config

# Modify the configuration files (example)
echo -e "\nModifying configuration files..."
echo "# Custom project name added" >> custom_config/crews.yaml

# Run a crew using the custom configuration
echo -e "\nRunning a crew using custom configuration..."
echo "This would execute the crew if you uncomment the following line:"
# pmoai run project_initiation_crew --config-dir custom_config --project-name "Custom Project" --output-dir output
