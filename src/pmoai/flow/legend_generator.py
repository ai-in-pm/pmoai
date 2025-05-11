"""
Legend generator for flow visualization.
"""

from typing import Dict, List

from pmoai.flow.config import FlowConfig


class LegendGenerator:
    """Generator for flow visualization legends.

    This class provides functionality for generating legend items for flow
    visualization.
    """

    def __init__(self, config: FlowConfig):
        """Initialize the legend generator.

        Args:
            config: The flow visualization configuration.
        """
        self.config = config
    
    def generate_legend_items(self) -> List[Dict[str, str]]:
        """Generate legend items for flow visualization.

        Returns:
            A list of legend items.
        """
        legend_items = []
        
        # Add node type legend items
        legend_items.append({
            "type": "color",
            "color": self.config.start_node_color,
            "label": "Start Node",
        })
        
        legend_items.append({
            "type": "color",
            "color": self.config.flow_node_color,
            "label": "Flow Node",
        })
        
        legend_items.append({
            "type": "color",
            "color": self.config.crew_node_color,
            "label": "Crew Node",
        })
        
        legend_items.append({
            "type": "color",
            "color": self.config.router_node_color,
            "label": "Router Node",
        })
        
        # Add edge type legend items
        legend_items.append({
            "type": "line",
            "style": "solid",
            "label": "Direct Flow",
        })
        
        legend_items.append({
            "type": "line",
            "style": "dashed",
            "label": "Conditional Flow",
        })
        
        # Add custom legend items
        for item in self.config.legend_items:
            legend_items.append(item)
        
        return legend_items
