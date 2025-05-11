"""
Utility functions for flow visualization.
"""

import json
from typing import Any, Dict, List, Optional

from pmoai.flow.config import FlowConfig


def create_node(
    id: str,
    label: str,
    node_type: str = "flow",
    config: Optional[FlowConfig] = None,
    **kwargs: Any,
) -> Dict[str, Any]:
    """Create a node for flow visualization.

    Args:
        id: The ID of the node.
        label: The label of the node.
        node_type: The type of the node (start, flow, crew, router).
        config: Optional configuration for visualization.
        **kwargs: Additional node properties.

    Returns:
        A dictionary representing the node.
    """
    if config is None:
        config = FlowConfig()
    
    # Determine node color and shape based on type
    color = config.flow_node_color
    shape = config.flow_node_shape
    
    if node_type == "start":
        color = config.start_node_color
        shape = config.start_node_shape
    elif node_type == "crew":
        color = config.crew_node_color
        shape = config.crew_node_shape
    elif node_type == "router":
        color = config.router_node_color
        shape = config.router_node_shape
    
    # Check for custom color and shape
    if id in config.custom_node_colors:
        color = config.custom_node_colors[id]
    
    if id in config.custom_node_shapes:
        shape = config.custom_node_shapes[id]
    
    # Create the node
    node = {
        "id": id,
        "label": label,
        "color": color,
        "shape": shape,
        "font": {
            "face": config.font_family,
            "size": config.font_size,
        },
        **kwargs,
    }
    
    return node


def create_edge(
    from_node: str,
    to_node: str,
    is_conditional: bool = False,
    condition_type: str = "",
    config: Optional[FlowConfig] = None,
    **kwargs: Any,
) -> Dict[str, Any]:
    """Create an edge for flow visualization.

    Args:
        from_node: The ID of the source node.
        to_node: The ID of the target node.
        is_conditional: Whether the edge is conditional.
        condition_type: The type of condition (and, or).
        config: Optional configuration for visualization.
        **kwargs: Additional edge properties.

    Returns:
        A dictionary representing the edge.
    """
    if config is None:
        config = FlowConfig()
    
    # Determine edge color and style based on type
    color = config.default_edge_color
    style = config.default_edge_style
    
    if is_conditional:
        color = config.conditional_edge_color
        style = config.conditional_edge_style
    
    # Check for custom color and style
    edge_id = f"{from_node}-{to_node}"
    if edge_id in config.custom_edge_colors:
        color = config.custom_edge_colors[edge_id]
    
    if edge_id in config.custom_edge_styles:
        style = config.custom_edge_styles[edge_id]
    
    # Create the edge
    edge = {
        "from": from_node,
        "to": to_node,
        "color": color,
        "dashes": style == "dashed",
        **kwargs,
    }
    
    # Add label for condition type
    if condition_type:
        edge["label"] = condition_type
        edge["font"] = {
            "face": config.font_family,
            "size": config.font_size,
            "align": "middle",
        }
    
    return edge


def generate_network_script(
    nodes: List[Dict[str, Any]],
    edges: List[Dict[str, Any]],
    config: Optional[FlowConfig] = None,
) -> str:
    """Generate a JavaScript script for visualizing a network.

    Args:
        nodes: The nodes of the network.
        edges: The edges of the network.
        config: Optional configuration for visualization.

    Returns:
        A JavaScript script for visualizing the network.
    """
    if config is None:
        config = FlowConfig()
    
    # Convert nodes and edges to JSON
    nodes_json = json.dumps(nodes)
    edges_json = json.dumps(edges)
    
    # Generate the script
    script = f"""
    <script type="text/javascript">
      // Create a network
      var container = document.getElementById("mynetwork");
      var data = {{
        nodes: new vis.DataSet({nodes_json}),
        edges: new vis.DataSet({edges_json})
      }};
      var options = {{
        nodes: {{
          shape: "box",
          margin: 10,
          widthConstraint: {{
            maximum: 200
          }},
          font: {{
            face: "{config.font_family}",
            size: {config.font_size}
          }}
        }},
        edges: {{
          arrows: "to",
          smooth: {{
            type: "cubicBezier",
            forceDirection: "horizontal",
            roundness: 0.4
          }}
        }},
        layout: {{
          hierarchical: {{
            enabled: {str(config.hierarchical).lower()},
            direction: "{config.direction}",
            nodeSpacing: {config.node_spacing},
            levelSeparation: {config.level_separation}
          }}
        }},
        physics: {{
          enabled: {str(config.physics_enabled).lower()},
          hierarchicalRepulsion: {{
            nodeDistance: 150
          }},
          solver: "hierarchicalRepulsion"
        }}
      }};
      var network = new vis.Network(container, data, options);
    </script>
    """
    
    return script
