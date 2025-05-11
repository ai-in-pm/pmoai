"""
Flow visualizer module for visualizing flow execution.
"""

import base64
import json
import logging
import os
import webbrowser
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union, cast

from pmoai.flow.config import FlowConfig
from pmoai.flow.flow_trackable import FlowTrackable
from pmoai.flow.html_template_handler import HTMLTemplateHandler
from pmoai.flow.legend_generator import LegendGenerator
from pmoai.flow.path_utils import get_assets_path
from pmoai.flow.utils import get_class_name
from pmoai.flow.visualization_utils import (
    create_edge,
    create_node,
    generate_network_script,
)

logger = logging.getLogger(__name__)


class FlowVisualizer:
    """Visualizer for flow execution.

    This class provides functionality for visualizing flow execution, including
    generating HTML visualizations of flow graphs.
    """

    def __init__(
        self,
        flow_trackable: FlowTrackable,
        config: Optional[FlowConfig] = None,
    ):
        """Initialize the flow visualizer.

        Args:
            flow_trackable: The flow trackable to visualize.
            config: Optional configuration for visualization.
        """
        self.flow_trackable = flow_trackable
        self.config = config or FlowConfig()
        self.template_handler = HTMLTemplateHandler()
        self.legend_generator = LegendGenerator(self.config)
    
    def visualize(self, output_path: Optional[str] = None, open_browser: bool = True) -> str:
        """Visualize the flow.

        Args:
            output_path: Optional path to save the visualization.
            open_browser: Whether to open the visualization in a browser.

        Returns:
            The path to the generated visualization.
        """
        # Generate nodes and edges
        nodes, edges = self._generate_nodes_and_edges()
        
        # Generate the network script
        network_script = generate_network_script(nodes, edges, self.config)
        
        # Generate the legend items
        legend_items = self.legend_generator.generate_legend_items()
        
        # Get the logo SVG
        logo_svg = self._get_logo_svg()
        
        # Generate the HTML
        html = self.template_handler.generate_html(
            title=self.config.title or f"{get_class_name(self.flow_trackable)} Flow",
            network_content=network_script,
            legend_items=legend_items,
            logo_svg_base64=logo_svg,
        )
        
        # Determine the output path
        if output_path is None:
            output_path = self.config.export_path or "flow_visualization.html"
        
        # Save the HTML
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)
        
        # Open the browser if requested
        if open_browser:
            webbrowser.open(f"file://{os.path.abspath(output_path)}")
        
        return output_path
    
    def _generate_nodes_and_edges(self) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """Generate nodes and edges for the flow.

        Returns:
            A tuple of (nodes, edges).
        """
        nodes = []
        edges = []
        
        # Get tracked methods
        tracked_methods = self.flow_trackable.get_tracked_methods()
        start_methods = self.flow_trackable.get_start_methods()
        trigger_methods = self.flow_trackable.get_trigger_methods()
        router_methods = self.flow_trackable.get_router_methods()
        condition_types = self.flow_trackable.get_condition_types()
        
        # Create nodes for all tracked methods
        for method_name in tracked_methods:
            # Determine node type
            node_type = "flow"
            if method_name in start_methods:
                node_type = "start"
            elif method_name in router_methods:
                node_type = "router"
            
            # Create the node
            node = create_node(
                id=method_name,
                label=method_name,
                node_type=node_type,
                config=self.config,
            )
            nodes.append(node)
        
        # Create edges for all trigger methods
        for source, targets in trigger_methods.items():
            for target in targets:
                # Determine if this is a conditional edge
                is_conditional = source in condition_types
                condition_type = condition_types.get(source, "")
                
                # Create the edge
                edge = create_edge(
                    from_node=source,
                    to_node=target,
                    is_conditional=is_conditional,
                    condition_type=condition_type,
                    config=self.config,
                )
                edges.append(edge)
        
        return nodes, edges
    
    def _get_logo_svg(self) -> str:
        """Get the logo SVG as a base64-encoded string.

        Returns:
            The base64-encoded logo SVG.
        """
        logo_path = Path(get_assets_path()) / "pmoai_logo.svg"
        if logo_path.exists():
            with open(logo_path, "rb") as f:
                return base64.b64encode(f.read()).decode("utf-8")
        else:
            logger.warning(f"Logo file not found at {logo_path}")
            return ""
