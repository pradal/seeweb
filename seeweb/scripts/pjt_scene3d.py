import json
from uuid import uuid1

from seeweb.models.content_item import ContentItem
from seeweb.models.project import Project


def main(session):
    """Create scene3d related projects.

    Args:
        session: (DBSession)

    Returns:
        None
    """
    scnpjt = Project.create(session, 'revesansparole', 'scene_pjt')
    scnpjt.public = True

    item = ContentItem.create(session, uuid1().hex, "scene3d", scnpjt)
    item.name = "multi box"
    item.author = "revesansparole"
    with open("seeweb/scripts/scene.json", 'r') as f:
        sc_def = json.load(f)
        item.store_definition(sc_def)
