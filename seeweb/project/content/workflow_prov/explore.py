"""Explore the content of a project to find its workflow nodes.
"""
from seeweb.io import find_definitions, load_schema
from seeweb.models.content_item import ContentItem


schema = load_schema(__file__)


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
    for pth, fname, idef in find_definitions(root_pth, schema, ["*.prov"]):
        prov = ContentItem.create(session,
                                  idef['id'],
                                  "workflow_prov",
                                  project)
        prov.author = idef['author']
        prov.name = idef['name']
        prov.store_description("Execution of workflow")
        prov.store_definition(idef)
