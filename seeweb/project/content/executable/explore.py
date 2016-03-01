"""Explore the content of a project to find its workflow nodes.
"""
from ConfigParser import ConfigParser
from os.path import exists
from os.path import join as pj
from uuid import uuid1

from seeweb.models.content_item import ContentItem


def explore_pth(session, root_pth, project):
    """Explore root_pth to find executable definitions.

    Fill project content with all elements recognized
    by the platform.

    Args:
        session: (DBSession)
        root_pth: (str) root dir to start exploring
        project: (Project)

    Returns:
        None
    """
    setup_pth = pj(root_pth, "setup.py")
    if not exists(setup_pth):
        return None

    egg_pth = pj(root_pth, "src", "%s.egg-info" % project.id)
    if not exists(egg_pth):
        return None

    cf = ConfigParser()
    cf.read(pj(egg_pth, "entry_points.txt"))
    if cf.has_section('console_scripts'):
        for ep_name, ep_loc in cf.items('console_scripts'):
            exe = ContentItem.create(session,
                                     uuid1().hex,
                                     "executable",
                                     project)
            exe.author = project.owner
            exe.name = ep_name
            exe.store_description(ep_loc)
            # exe.store_definition(ep)
