"""Add a crew to a flow."""

import os
import sys
from pathlib import Path

import click

from pmoai.cli.create_crew import create_crew
from pmoai.cli.utils import find_config_dir


def add_crew_to_flow(crew_name):
    """Add a crew to a flow.
    
    Args:
        crew_name: The name of the crew to add.
    """
    # Find the flow directory
    flow_dir = Path.cwd()
    
    # Check if this is a flow directory
    flow_file = flow_dir / "flow.py"
    if not flow_file.exists():
        # Check if this is a project directory with a flow.py file
        flow_file = flow_dir / "src" / flow_dir.name / "flow.py"
        if not flow_file.exists():
            click.secho("Error: Could not find flow.py file.", fg="red")
            click.secho("Please run this command from a flow directory.", fg="red")
            sys.exit(1)
    
    # Create the crews directory if it doesn't exist
    crews_dir = flow_dir / "crews"
    if not crews_dir.exists():
        crews_dir = flow_dir / "src" / flow_dir.name / "crews"
        if not crews_dir.exists():
            crews_dir.mkdir(parents=True)
    
    # Create the crew
    create_crew(crew_name, skip_provider=True, parent_folder=crews_dir)
    
    # Update the flow.py file to import the crew
    with open(flow_file, "r") as f:
        flow_content = f.read()
    
    # Check if the crew is already imported
    import_line = f"from .crews.{crew_name.lower().replace(' ', '_').replace('-', '_')}.crew import {crew_name.replace(' ', '').replace('-', '')}"
    if import_line not in flow_content:
        # Add the import
        import_section_end = flow_content.find("\n\n")
        if import_section_end == -1:
            import_section_end = 0
        
        flow_content = flow_content[:import_section_end] + f"\n{import_line}" + flow_content[import_section_end:]
        
        # Add the crew to the flow
        flow_class_start = flow_content.find("class ")
        if flow_class_start != -1:
            flow_class_end = flow_content.find(":", flow_class_start)
            if flow_class_end != -1:
                flow_class_name = flow_content[flow_class_start + 6:flow_class_end].strip()
                
                # Find the crews list
                crews_list_start = flow_content.find("crews = [", flow_class_end)
                if crews_list_start != -1:
                    crews_list_end = flow_content.find("]", crews_list_start)
                    if crews_list_end != -1:
                        # Add the crew to the list
                        crew_class_name = crew_name.replace(" ", "").replace("-", "")
                        if crew_class_name not in flow_content[crews_list_start:crews_list_end]:
                            flow_content = flow_content[:crews_list_end] + f", {crew_class_name}()" + flow_content[crews_list_end:]
                else:
                    # No crews list found, add it
                    flow_class_body_start = flow_content.find("\n", flow_class_end)
                    if flow_class_body_start != -1:
                        crew_class_name = crew_name.replace(" ", "").replace("-", "")
                        flow_content = flow_content[:flow_class_body_start + 1] + f"    crews = [{crew_class_name}()]\n" + flow_content[flow_class_body_start + 1:]
        
        # Write the updated flow.py file
        with open(flow_file, "w") as f:
            f.write(flow_content)
    
    click.secho(f"Crew {crew_name} added to flow successfully!", fg="green", bold=True)
