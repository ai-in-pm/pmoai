"""
Utility functions for flow visualization.
"""

import inspect
from typing import Any, Dict, List, Optional, Set, Tuple, Union, cast


def get_class_name(obj: Any) -> str:
    """Get the class name of an object.

    Args:
        obj: The object to get the class name of.

    Returns:
        The class name of the object.
    """
    return obj.__class__.__name__


def get_method_name(method: Any) -> str:
    """Get the name of a method.

    Args:
        method: The method to get the name of.

    Returns:
        The name of the method.
    """
    return method.__name__


def get_method_signature(method: Any) -> str:
    """Get the signature of a method.

    Args:
        method: The method to get the signature of.

    Returns:
        The signature of the method.
    """
    return str(inspect.signature(method))


def get_method_doc(method: Any) -> str:
    """Get the docstring of a method.

    Args:
        method: The method to get the docstring of.

    Returns:
        The docstring of the method.
    """
    return inspect.getdoc(method) or ""


def get_method_source(method: Any) -> str:
    """Get the source code of a method.

    Args:
        method: The method to get the source code of.

    Returns:
        The source code of the method.
    """
    try:
        return inspect.getsource(method)
    except (TypeError, OSError):
        return ""


def get_method_file(method: Any) -> str:
    """Get the file containing a method.

    Args:
        method: The method to get the file of.

    Returns:
        The file containing the method.
    """
    try:
        return inspect.getfile(method)
    except (TypeError, OSError):
        return ""


def get_method_line(method: Any) -> int:
    """Get the line number of a method.

    Args:
        method: The method to get the line number of.

    Returns:
        The line number of the method.
    """
    try:
        return inspect.getsourcelines(method)[1]
    except (TypeError, OSError):
        return 0
