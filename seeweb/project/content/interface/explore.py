"""Explore the content of a project to find its workflow nodes.
"""
import json
from os import walk
from os.path import splitext
from os.path import join as pj

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
    for root, dirnames, filenames in walk(root_pth):
        # avoid hidden directories
        for i in range(len(dirnames) - 1, -1, -1):
            if dirnames[i].startswith("."):
                del dirnames[i]

        # find recognized content items
        for fname in filenames:
            if splitext(fname)[1] == ".json":
                pth = pj(root, fname)
                with open(pth, 'r') as f:
                    idef = json.load(f)

                if idef.get("category", "") == "oainterface":
                    node = ContentItem.create(session,
                                              idef['id'],
                                              "interface",
                                              project)
                    node.author = idef['author']
                    node.name = idef['name']
                    node.store_description(idef['description'])
                    node.store_definition(idef)
