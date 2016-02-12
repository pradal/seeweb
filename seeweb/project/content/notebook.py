"""Set of functions to explore the content of notebook.
"""

from os.path import basename, splitext


def can_handle_file(pth):
    """Check if file path correspond to a notebook file.

    Args:
        pth: (str)

    Returns:
        (bool) whether notebooks knows how to handle this file
    """
    return splitext(pth)[1] == ".ipynb"


def analyse(pth):
    """Open notebook file to extract a notebook description.

    Args:
        pth: (str)

    Returns:
        (dict of str, any): notebook description
    """
    return basename(pth)
