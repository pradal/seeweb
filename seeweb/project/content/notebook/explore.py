"""Explore the content of a project to find its workflow nodes.
"""
import json
import nbformat
from uuid import uuid1

from seeweb.io import find_files
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
    for pth, fname in find_files(root_pth, ["*.ipynb"]):
        try:
            with open(pth, 'r') as f:
                nbdef = json.load(f)
                try:
                    nbformat.validate(nbdef)
                    # create notebook content
                    nb = ContentItem.create(session,
                                            uuid1().hex,
                                            "notebook",
                                            project)
                    nb.author = project.owner
                    nb.name = fname[:-6]
                    nb.store_description(pth)
                    nb.store_definition(nbdef)
                except nbformat.ValidationError:
                    print "%s not a real notebook" % fname
        except ValueError:
            print "unable to load %s" % fname
