"""Explore the content of a project to find its workflow nodes.
"""
import json

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
    for pth, fname in find_files(root_pth, ["*.json"]):
        with open(pth, 'r') as f:
            sc_def = json.load(f)

        if sc_def.get("metadata", {}).get("type", "") == "Object":
            obj = sc_def['object']
            node = ContentItem.create(session,
                                      obj['uuid'],
                                      "scene3d",
                                      project)
            node.author = project.owner
            node.name = obj['name']
            node.store_description("three.js")
            node.store_definition(sc_def)
