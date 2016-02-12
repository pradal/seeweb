"""Set of functions to explore the content of workflow nodes.
"""

import json
from os.path import splitext


def can_handle_file(pth):
    """Check if file path correspond to a node definition file.

    Args:
        pth: (str)

    Returns:
        (bool) whether workflow nodes knows how to handle this file
    """
    if splitext(pth)[1] == ".json":
        with open(pth, 'r') as f:
            node_def = json.load(f)
            return "category" in node_def and node_def["category"] == "oanode"

    return False


def analyse(pth):
    """Open node definition file.

    Args:
        pth: (str)

    Returns:
        (dict of str, any): node description
    """
    with open(pth, 'r') as f:
        node_def = json.load(f)

    return node_def['name']
