"""Set of functions used to manage avatars
"""
import os
from os.path import dirname, exists, join
from PIL import Image
import StringIO


def _avatar_pth(item, item_type, small=False):
    """Return the path to an avatar.

    Warnings: does not test if path exists

    Args:
        item: (Project|Team|User)
        item_type: (str) name of item
        small: (Bool) default False, avatar have two sizes

    Returns:
        (str): pth to avatar file
    """
    root = dirname(__file__)
    if small:
        name = "%s_small.png" % item.id
    else:
        name = "%s.png" % item.id

    return join(root, "data", "avatar", item_type, name)


def project_avatar_pth(project, small=False):
    """Return the path to a project avatar.

    Warnings: does not test if path exists

    Args:
        project: (Project)
        small: (Bool) default False, avatar have two sizes

    Returns:
        (str): pth to avatar file
    """
    return _avatar_pth(project, "project", small)


def team_avatar_pth(team, small=False):
    """Return the path to a team avatar.

    Warnings: does not test if path exists

    Args:
        team: (Team)
        small: (Bool) default False, avatar have two sizes

    Returns:
        (str): pth to avatar file
    """
    return _avatar_pth(team, "team", small)


def user_avatar_pth(user, small=False):
    """Return the path to a user avatar.

    Warnings: does not test if path exists

    Args:
        user: (User)
        small: (Bool) default False, avatar have two sizes

    Returns:
        (str): pth to avatar file
    """
    return _avatar_pth(user, "user", small)


def load_image(field_storage):
    """Generate an image from data in field_storage

    Args:
        field_storage: (FieldStorage) html structure

    Returns:
        (Image)
    """
    input_file = field_storage.file
    input_file.seek(0)
    img = Image.open(StringIO.StringIO(input_file.read()))

    return img


def _upload_avatar(img, item, item_type):
    """Upload an image to use as an avatar.

    Args:
        img: (Image)
        item: (Project|Team|User)
        item_type: (str) name of item

    Returns:
        None
    """
    s = 256
    thumb = Image.new('RGBA', (s, s))
    img.thumbnail((s, s))
    thumb.paste(img, ((s - img.size[0]) / 2, (s - img.size[1]) / 2))

    pth = _avatar_pth(item, item_type, small=False)

    if exists(pth):
        os.remove(pth)
    thumb.save(pth)

    s = 64
    thumb = Image.new('RGBA', (s, s))
    img.thumbnail((s, s))
    thumb.paste(img, ((s - img.size[0]) / 2, (s - img.size[1]) / 2))

    pth = _avatar_pth(item, item_type, small=True)

    if exists(pth):
        os.remove(pth)
    thumb.save(pth)


def upload_project_avatar(img, project):
    """Upload an image to use as project avatar.

    Args:
        img: (Image)
        project: (Project)

    Returns:
        None
    """
    _upload_avatar(img, project, 'project')


def upload_team_avatar(img, team):
    """Upload an image to use as team avatar.

    Args:
        img: (Image)
        team: (Team)

    Returns:
        None
    """
    _upload_avatar(img, team, 'team')


def upload_user_avatar(img, user):
    """Upload an image to use as user avatar.

    Args:
        img: (Image)
        user: (User)

    Returns:
        None
    """
    _upload_avatar(img, user, 'user')


def _generate_default_avatar(item, item_type):
    root = dirname(__file__)
    pth = join(root, "static", "%s_avatar.png" % item_type)  # better files
    img = Image.open(pth)
    _upload_avatar(img, item, item_type)


def generate_default_project_avatar(project):
    """Upload a default avatar for a project.

    Args:
        project: (Project)

    Returns:
        None
    """
    _generate_default_avatar(project, 'project')


def generate_default_team_avatar(team):
    """Upload a default avatar for a team.

    Args:
        team: (Team)

    Returns:
        None
    """
    _generate_default_avatar(team, 'team')


def generate_default_user_avatar(user):
    """Upload a default avatar for a user.

    Args:
        user: (User)

    Returns:
        None
    """
    _generate_default_avatar(user, 'user')


def _remove_avatar(item, item_typ):
    for pth in (_avatar_pth(item, item_typ),
                _avatar_pth(item, item_typ, True)):
        if exists(pth):
            os.remove(pth)


def remove_project_avatar(project):
    """Remove avatar files associated to a project.

    Args:
        project: (Project)

    Returns:
        (None)
    """
    _remove_avatar(project, 'project')


def remove_team_avatar(team):
    """Remove avatar files associated to a team.

    Args:
        team: (Team)

    Returns:
        (None)
    """
    _remove_avatar(team, 'team')


def remove_user_avatar(user):
    """Remove avatar files associated to a user.

    Args:
        user: (User)

    Returns:
        (None)
    """
    _remove_avatar(user, 'user')
