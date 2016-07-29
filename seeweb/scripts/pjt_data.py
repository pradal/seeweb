from seeweb.models.ro_link import ROLink
from seeweb.ro.container.models.ro_container import ROContainer
from seeweb.ro.data.models.ro_data import ROData
from seeweb.rodata.image.models.ro_image import ROImage
from seeweb.rodata.scene3d.models.ro_scene3d import ROScene3d


def main(session, user, container):
    """Create a project that contains different types of data

    Args:
        session (DBSession):
        user (User): owner of created project
        container (ROContainer): top level container

    Returns:
        None
    """
    roc = ROContainer()
    roc.init(session, dict(owner=user.id, name="data"))
    ROLink.connect(session, container.id, roc.id, 'contains')

    # raw data
    with open("seeweb/ro/data/static/default_avatar.png", 'rb') as f:
        value = f.read()

    rod = ROData()
    rod.init(session, dict(owner=user.id, name="test data", value=value))
    ROLink.connect(session, roc.id, rod.id, "contains")

    # image
    with open("seeweb/rodata/image/static/default_avatar.png", 'rb') as f:
        value = f.read()

    roi = ROImage()
    roi.init(session, dict(owner=user.id, name="test image", value=value))
    ROLink.connect(session, roc.id, roi.id, "contains")

    # scene3D
    with open("seeweb/scripts/scene.json", 'r') as f:
        sc = f.read()

    rosc = ROScene3d()
    rosc.init(session, dict(owner=user.id, name="test scene", scene=sc))
    ROLink.connect(session, roc.id, rosc.id, "contains")
