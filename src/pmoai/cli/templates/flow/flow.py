from pmoai import Flow
from pmoai.project import FlowBase, flow

@FlowBase
class {{class_name}}():
    """{{class_name}} flow"""
    
    # Project Management specific properties
    project_name: str = "Project Name"
    project_code: str = "PRJ-001"
    project_methodology: str = "Agile"
    project_phase: str = "Planning"
    organization: str = "Organization Name"
    portfolio: str = "Portfolio Name"
    
    # Add your crews here
    crews = []
    
    @flow
    def flow(self) -> Flow:
        """Creates the {{class_name}} flow"""
        return Flow(
            crews=self.crews,
            name="{{class_name}}",
            description="{{class_name}} flow",
        )
