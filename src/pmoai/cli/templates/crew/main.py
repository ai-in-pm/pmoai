#!/usr/bin/env python3
"""Main entry point for the {{crew_name}} crew."""

import argparse
import os
import sys

from {{folder_name}}.crew import {{crew_name}}


def main():
    """Run the {{crew_name}} crew."""
    parser = argparse.ArgumentParser(description="{{crew_name}} - A PMOAI crew")
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
        print("Please set it before running the crew.")
        return 1
    
    # Create the crew
    crew = {{crew_name}}()
    
    # Update crew properties
    crew.project_name = args.project_name
    crew.project_code = args.project_code
    crew.project_methodology = args.methodology
    crew.project_phase = args.phase
    crew.organization = args.organization
    crew.portfolio = args.portfolio
    
    # Execute crew
    print(f"=== Executing {{crew_name}} Crew ===")
    print(f"Project: {crew.project_name}")
    print(f"Methodology: {crew.project_methodology}")
    print(f"Phase: {crew.project_phase}")
    print()
    
    try:
        result = crew.kickoff()
    except Exception as e:
        print(f"Error executing crew: {e}")
        return 1
    
    # Print results
    print("\n=== Execution Results ===\n")
    print(result.raw)
    
    # Save results to files
    os.makedirs(args.output_dir, exist_ok=True)
    
    for i, task_output in enumerate(result.tasks_output):
        task_name = task_output.task.description.split()[0].lower()
        filename = os.path.join(args.output_dir, f"output_{i+1}_{task_name}.md")
        
        with open(filename, "w") as f:
            f.write(task_output.raw)
        
        print(f"Saved {filename}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
