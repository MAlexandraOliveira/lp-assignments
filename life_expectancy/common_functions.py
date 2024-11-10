import os


def get_base_directory() -> str:
    """
    Determines the base directory where the script is located.
    """
    return os.path.dirname(os.path.abspath(__file__))
