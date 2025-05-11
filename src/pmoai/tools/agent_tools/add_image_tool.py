import base64
import logging
import os
from typing import Optional

from pydantic import Field

from pmoai.tools.agent_tools.base_agent_tools import BaseAgentTool

logger = logging.getLogger(__name__)


class AddImageTool(BaseAgentTool):
    """
    Tool for adding images to the conversation.
    """

    name: str = Field(default="add_image", description="Name of the tool")
    description: str = Field(
        default="Add an image to the conversation. Use this when you want to include an image in your response.",
        description="Description of the tool",
    )

    def _run(
        self,
        image_path: Optional[str] = None,
        image_url: Optional[str] = None,
        image_base64: Optional[str] = None,
        alt_text: Optional[str] = None,
        **kwargs,
    ) -> str:
        """
        Add an image to the conversation.

        Args:
            image_path: Local path to the image file
            image_url: URL of the image
            image_base64: Base64-encoded image data
            alt_text: Alternative text for the image
            **kwargs: Additional arguments

        Returns:
            Markdown-formatted image tag
        """
        alt_text = alt_text or "Image"

        if image_url:
            return f"![{alt_text}]({image_url})"
        
        if image_path:
            if not os.path.exists(image_path):
                return self.i18n.errors("image_tool_file_not_found").format(path=image_path)
            
            try:
                with open(image_path, "rb") as image_file:
                    image_data = image_file.read()
                    image_base64 = base64.b64encode(image_data).decode("utf-8")
                    
                    # Determine MIME type based on file extension
                    _, ext = os.path.splitext(image_path)
                    mime_type = self._get_mime_type(ext)
                    
                    return f"![{alt_text}](data:{mime_type};base64,{image_base64})"
            except Exception as e:
                logger.error(f"Error reading image file: {e}")
                return self.i18n.errors("image_tool_read_error").format(error=str(e))
        
        if image_base64:
            # Try to determine if MIME type is included
            if "data:" in image_base64 and ";base64," in image_base64:
                return f"![{alt_text}]({image_base64})"
            else:
                # Assume PNG if no MIME type is provided
                return f"![{alt_text}](data:image/png;base64,{image_base64})"
        
        return self.i18n.errors("image_tool_missing_image")
    
    def _get_mime_type(self, extension: str) -> str:
        """
        Get the MIME type for a file extension.
        
        Args:
            extension: File extension including the dot
            
        Returns:
            MIME type string
        """
        extension = extension.lower()
        mime_types = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".gif": "image/gif",
            ".bmp": "image/bmp",
            ".webp": "image/webp",
            ".svg": "image/svg+xml",
        }
        
        return mime_types.get(extension, "image/png")
