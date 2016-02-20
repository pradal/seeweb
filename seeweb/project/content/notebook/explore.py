"""Explore the content of a project to find its workflow nodes.
"""
import json
from os import walk
from os.path import splitext
from os.path import join as pj
from uuid import uuid1

from seeweb.models.content_item import ContentItem


def explore_pth(session, root_pth, project):
    """Explore recursively pth to find notebooks.

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
            nb_name, ext = splitext(fname)
            if ext == ".ipynb":
                nb = ContentItem.create(session,
                                        uuid1().hex,
                                        "notebook",
                                        project)
                nb.author = project.owner
                nb.name = nb_name
                nb.store_description(pj(root, fname))
                nb.store_definition("")
