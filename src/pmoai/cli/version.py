from importlib.metadata import version as get_version


def get_pmoai_version() -> str:
    """
    Get the version of PMOAI.

    Returns:
        The version of PMOAI.
    """
    try:
        return get_version("pmoai")
    except Exception:
        return "unknown version"
