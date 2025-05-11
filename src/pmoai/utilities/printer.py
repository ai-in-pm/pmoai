"""Printer utilities for PMOAI."""

import sys
from typing import Dict, Optional, TextIO


class Printer:
    """A utility class for printing colored text to the console."""

    # ANSI color codes
    COLORS: Dict[str, str] = {
        "black": "\033[30m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
        "reset": "\033[0m",
        "bold": "\033[1m",
    }

    def __init__(self, enable_colors: bool = True):
        """Initialize the printer.
        
        Args:
            enable_colors: Whether to enable colored output.
        """
        self.enable_colors = enable_colors and sys.stdout.isatty()

    def print(
        self,
        text: str,
        color: Optional[str] = None,
        bold: bool = False,
        file: TextIO = sys.stdout,
    ) -> None:
        """Print text with optional color and formatting.
        
        Args:
            text: The text to print.
            color: The color to use.
            bold: Whether to print in bold.
            file: The file to print to.
        """
        if self.enable_colors and (color or bold):
            formatted_text = ""
            if bold:
                formatted_text += self.COLORS["bold"]
            if color and color in self.COLORS:
                formatted_text += self.COLORS[color]
            
            formatted_text += text + self.COLORS["reset"]
            print(formatted_text, file=file)
        else:
            print(text, file=file)
