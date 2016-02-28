"""Explore the content of a project to find its workflow nodes.
"""
import json
from jsonschema import validate, ValidationError
from os import walk
from os.path import dirname, splitext
from os.path import join as pj

from seeweb.models.content_item import ContentItem


with open(pj(dirname(__file__), "schema.json"), 'r') as f:
    schema = json.load(f)


def check_definition(idef):
    try:
        validate(idef, schema)
        return True
    except ValidationError:
        return False


def explore_pth(session, root_pth, project):
    """Explore recursively pth to find workflow provenance definitions.

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
            if splitext(fname)[1] == ".prov":
                pth = pj(root, fname)
                with open(pth, 'r') as f:
                    pdef = json.load(f)

                if check_definition(pdef):
                    prov = ContentItem.create(session,
                                              pdef['id'],
                                              "workflow_prov",
                                              project)
                    prov.author = pdef['author']
                    prov.name = pdef['name']
                    prov.store_description("Execution of workflow")
                    prov.store_definition(pdef)
                    prov.extra = pdef['workflow']
