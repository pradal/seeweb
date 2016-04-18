"""Explore the content of a project to find its workflow nodes.
"""
import json
from openalea.wlformat.workflow import validate

from seeweb.io import find_files
from seeweb.models.content_item import ContentItem


def explore_pth(session, root_pth, project):
    """Explore recursively pth to find workflow definitions.

    Fill project content with all elements recognized
    by the platform.

    Args:
        session: (DBSession)
        root_pth: (str) root dir to start exploring
        project: (Project)

    Returns:
        None
    """
    for pth, fname in find_files(root_pth, ["*.wkf"]):
        with open(pth, 'r') as f:
            wdef = json.load(f)
            if validate(wdef):
                ContentItem.create_from_def(session, "workflow", wdef, project)
