"""Explore the content of a project to find its workflow nodes.
"""
import json
from jsonschema import validate, ValidationError
from os.path import dirname
from os.path import join as pj

from seeweb.io import find_files
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
    """Explore recursively pth to find node definitions.

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
            node_def = json.load(f)

        if check_definition(node_def):
            node = ContentItem.create(session,
                                      node_def['id'],
                                      "workflow_node",
                                      project)
            node.author = node_def['author']
            node.name = node_def['name']
            node.store_description(node_def['description'])
            node.store_definition(node_def)
