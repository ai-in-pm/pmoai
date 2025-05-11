"""Logging utilities for PMOAI."""

import logging
import os
import sys
from typing import Optional


class Logger:
    """
    A simple logger for PMOAI.
    """

    def __init__(
        self,
        name: str = "pmoai",
        level: int = logging.INFO,
        log_file: Optional[str] = None,
    ):
        """
        Initialize the logger.

        Args:
            name: Logger name
            level: Logging level
            log_file: Optional path to log file
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # Create formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        
        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # Create file handler if log_file is provided
        if log_file:
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def debug(self, message: str) -> None:
        """Log a debug message."""
        self.logger.debug(message)
    
    def info(self, message: str) -> None:
        """Log an info message."""
        self.logger.info(message)
    
    def warning(self, message: str) -> None:
        """Log a warning message."""
        self.logger.warning(message)
    
    def error(self, message: str) -> None:
        """Log an error message."""
        self.logger.error(message)
    
    def critical(self, message: str) -> None:
        """Log a critical message."""
        self.logger.critical(message)
