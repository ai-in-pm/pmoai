"""
HTML template handler for flow visualization.
"""

import logging
import os
from pathlib import Path
from typing import Dict, List, Optional

from pmoai.flow.path_utils import get_assets_path

logger = logging.getLogger(__name__)


class HTMLTemplateHandler:
    """Handler for HTML templates.

    This class provides functionality for loading and rendering HTML templates
    for flow visualization.
    """

    def __init__(self, template_path: Optional[str] = None):
        """Initialize the HTML template handler.

        Args:
            template_path: Optional path to the HTML template.
        """
        if template_path is None:
            template_path = os.path.join(get_assets_path(), "pmoai_flow_visual_template.html")
        
        self.template_path = template_path
        self.template = self._load_template()
    
    def _load_template(self) -> str:
        """Load the HTML template.

        Returns:
            The HTML template.
        """
        try:
            with open(self.template_path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            logger.warning(f"Template file not found at {self.template_path}")
            return self._get_default_template()
    
    def _get_default_template(self) -> str:
        """Get the default HTML template.

        Returns:
            The default HTML template.
        """
        return """<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>{{ title }}</title>
    <script
      src="https://cdnjs.cloudflare.com/ajax/libs/vis-network/9.1.2/dist/vis-network.min.js"
      integrity="sha512-LnvoEWDFrqGHlHmDD2101OrLcbsfkrzoSpvtSQtxK3RMnRV0eOkhhBN2dXHKRrUU8p2DGRTk35n4O8nWSVe1mQ=="
      crossorigin="anonymous"
      referrerpolicy="no-referrer"
    ></script>
    <link
      rel="stylesheet"
      href="https://cdnjs.cloudflare.com/ajax/libs/vis-network/9.1.2/dist/dist/vis-network.min.css"
      integrity="sha512-WgxfT5LWjfszlPHXRmBWHkV2eceiWTOBvrKCNbdgDYTHrT2AeLCGbF4sZlZw3UMN3WtL0tGUoIAKsu8mllg/XA=="
      crossorigin="anonymous"
      referrerpolicy="no-referrer"
    />
    <style type="text/css">
      body {
        font-family: verdana;
        margin: 0;
        padding: 0;
      }
      .container {
        display: flex;
        flex-direction: column;
        height: 100vh;
      }
      #mynetwork {
        flex-grow: 1;
        width: 100%;
        height: 750px;
        background-color: #ffffff;
      }
      .card {
        border: none;
      }
      .legend-container {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 10px;
        background-color: #f8f9fa;
        position: fixed; /* Make the legend fixed */
        bottom: 0; /* Position it at the bottom */
        width: 100%; /* Make it span the full width */
      }
      .legend-item {
        display: flex;
        align-items: center;
        margin-right: 20px;
      }
      .legend-color-box {
        width: 20px;
        height: 20px;
        margin-right: 5px;
      }
      .logo {
        height: 50px;
        margin-right: 20px;
      }
      .legend-dashed {
        border-bottom: 2px dashed #666666;
        width: 20px;
        height: 0;
        margin-right: 5px;
      }
      .legend-solid {
        border-bottom: 2px solid #666666;
        width: 20px;
        height: 0;
        margin-right: 5px;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <div class="card" style="width: 100%">
        <div id="mynetwork" class="card-body"></div>
      </div>
      <div class="legend-container">
        <img
          src="data:image/svg+xml;base64,{{ logo_svg_base64 }}"
          alt="PMOAI logo"
          class="logo"
        />
        <!-- LEGEND_ITEMS_PLACEHOLDER -->
      </div>
    </div>
    {{ network_content }}
  </body>
</html>
"""
    
    def generate_html(
        self,
        title: str,
        network_content: str,
        legend_items: List[Dict[str, str]],
        logo_svg_base64: str,
    ) -> str:
        """Generate HTML for flow visualization.

        Args:
            title: The title of the visualization.
            network_content: The network content script.
            legend_items: The legend items.
            logo_svg_base64: The base64-encoded logo SVG.

        Returns:
            The generated HTML.
        """
        # Replace placeholders in the template
        html = self.template.replace("{{ title }}", title)
        html = html.replace("{{ network_content }}", network_content)
        html = html.replace("{{ logo_svg_base64 }}", logo_svg_base64)
        
        # Generate legend items HTML
        legend_items_html = ""
        for item in legend_items:
            if item["type"] == "color":
                legend_items_html += f"""
                <div class="legend-item">
                  <div class="legend-color-box" style="background-color: {item['color']}"></div>
                  <span>{item['label']}</span>
                </div>
                """
            elif item["type"] == "line":
                legend_items_html += f"""
                <div class="legend-item">
                  <div class="legend-{item['style']}"></div>
                  <span>{item['label']}</span>
                </div>
                """
        
        # Replace legend items placeholder
        html = html.replace("<!-- LEGEND_ITEMS_PLACEHOLDER -->", legend_items_html)
        
        return html
