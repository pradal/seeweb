import json
from uuid import uuid1

from seeweb.models.content_item import ContentItem
from seeweb.models.project import Project


def main(session):
    """Create notebook related projects.

    Args:
        session: (DBSession)

    Returns:
        None
    """
    notebook = Project.create(session, 'revesansparole', 'notebook_pjt')
    notebook.public = True

    for i in range(5):
        item = ContentItem.create(session, uuid1().hex, "notebook",
                                  notebook)
        item.name = "notebook%d" % i
        item.author = "revesansparole"

    item = ContentItem.create(session, uuid1().hex, "notebook", notebook)
    item.name = "real notebook"
    item.author = "revesansparole"
    with open("seeweb/scripts/notebook.ipynb", 'r') as f:
        notebook_def = json.load(f)
        item.store_definition(notebook_def)
