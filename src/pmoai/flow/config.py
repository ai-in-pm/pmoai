"""
Configuration for flow visualization.
"""

from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class FlowConfig(BaseModel):
    """Configuration for flow visualization.

    This class defines the configuration options for flow visualization,
    including colors, shapes, and other visual properties.
    """

    # Node colors
    start_node_color: str = Field(default="#4CAF50", description="Color for start nodes")
    flow_node_color: str = Field(default="#2196F3", description="Color for flow nodes")
    crew_node_color: str = Field(default="#FF9800", description="Color for crew nodes")
    router_node_color: str = Field(default="#9C27B0", description="Color for router nodes")
    
    # Edge colors
    default_edge_color: str = Field(default="#666666", description="Default color for edges")
    conditional_edge_color: str = Field(default="#E91E63", description="Color for conditional edges")
    
    # Node shapes
    start_node_shape: str = Field(default="diamond", description="Shape for start nodes")
    flow_node_shape: str = Field(default="box", description="Shape for flow nodes")
    crew_node_shape: str = Field(default="ellipse", description="Shape for crew nodes")
    router_node_shape: str = Field(default="hexagon", description="Shape for router nodes")
    
    # Edge styles
    default_edge_style: str = Field(default="solid", description="Default style for edges")
    conditional_edge_style: str = Field(default="dashed", description="Style for conditional edges")
    
    # Layout options
    hierarchical: bool = Field(default=True, description="Whether to use hierarchical layout")
    direction: str = Field(default="UD", description="Direction of hierarchical layout (UD, DU, LR, RL)")
    node_spacing: int = Field(default=100, description="Spacing between nodes")
    level_separation: int = Field(default=150, description="Separation between levels")
    
    # Legend options
    show_legend: bool = Field(default=True, description="Whether to show the legend")
    legend_position: str = Field(default="bottom", description="Position of the legend (top, bottom, left, right)")
    
    # Custom node colors
    custom_node_colors: Dict[str, str] = Field(
        default_factory=dict, description="Custom colors for specific nodes"
    )
    
    # Custom edge colors
    custom_edge_colors: Dict[str, str] = Field(
        default_factory=dict, description="Custom colors for specific edges"
    )
    
    # Custom node shapes
    custom_node_shapes: Dict[str, str] = Field(
        default_factory=dict, description="Custom shapes for specific nodes"
    )
    
    # Custom edge styles
    custom_edge_styles: Dict[str, str] = Field(
        default_factory=dict, description="Custom styles for specific edges"
    )
    
    # Title
    title: Optional[str] = Field(default=None, description="Title for the visualization")
    
    # Font options
    font_family: str = Field(default="arial", description="Font family for labels")
    font_size: int = Field(default=14, description="Font size for labels")
    
    # Size options
    width: str = Field(default="100%", description="Width of the visualization")
    height: str = Field(default="750px", description="Height of the visualization")
    
    # Physics options
    physics_enabled: bool = Field(default=True, description="Whether to enable physics simulation")
    
    # Export options
    export_format: str = Field(default="html", description="Format for exporting the visualization")
    export_path: Optional[str] = Field(default=None, description="Path for exporting the visualization")
    
    # Legend items
    legend_items: List[Dict[str, str]] = Field(
        default_factory=list, description="Custom legend items"
    )
