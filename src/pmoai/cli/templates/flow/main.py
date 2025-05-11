#!/usr/bin/env python3
"""Main entry point for the {{class_name}} flow."""

import argparse
import os
import sys

from {{folder_name}}.flow import {{class_name}}


def main():
    """Run the {{class_name}} flow."""
    parser = argparse.ArgumentParser(description="{{class_name}} - A PMOAI flow")
    parser.add_argument(
        "--project-name",
        default="Project Name",
        help="Project name",
    )
    parser.add_argument(
        "--project-code",
        default="PRJ-001",
        help="Project code",
    )
    parser.add_argument(
        "--methodology",
        default="Agile",
        help="Project management methodology",
    )
    parser.add_argument(
        "--phase",
        default="Planning",
        help="Project phase",
    )
    parser.add_argument(
        "--organization",
        default="Organization Name",
        help="Organization name",
    )
    parser.add_argument(
        "--portfolio",
        default="Portfolio Name",
        help="Portfolio name",
    )
    parser.add_argument(
        "--output-dir",
        default="output",
        help="Directory to save output files",
    )
    
    args = parser.parse_args()
    
    # Check if OpenAI API key is set
    if not os.environ.get("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable is not set.")
        print("Please set it before running the flow.")
        return 1
    
    # Create the flow
    flow = {{class_name}}()
    
    # Update flow properties
    flow.project_name = args.project_name
    flow.project_code = args.project_code
    flow.project_methodology = args.methodology
    flow.project_phase = args.phase
    flow.organization = args.organization
    flow.portfolio = args.portfolio
    
    # Execute flow
    print(f"=== Executing {{class_name}} Flow ===")
    print(f"Project: {flow.project_name}")
    print(f"Methodology: {flow.project_methodology}")
    print(f"Phase: {flow.project_phase}")
    print()
    
    try:
        result = flow.kickoff()
    except Exception as e:
        print(f"Error executing flow: {e}")
        return 1
    
    # Print results
    print("\n=== Execution Results ===\n")
    print(result.raw)
    
    # Save results to files
    os.makedirs(args.output_dir, exist_ok=True)
    
    for i, crew_output in enumerate(result.crews_output):
        crew_name = crew_output.crew.__class__.__name__.lower()
        filename = os.path.join(args.output_dir, f"output_{i+1}_{crew_name}.md")
        
        with open(filename, "w") as f:
            f.write(crew_output.raw)
        
        print(f"Saved {filename}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
