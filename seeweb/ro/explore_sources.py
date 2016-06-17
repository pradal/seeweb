"""Set of function to explore sources of a project and retrieve
relevant items.
"""

from os import listdir
from os.path import exists, splitext
from os.path import join as pj
from PIL import Image


def fetch_avatar(pth):
    """Find avatar file at the root of source dir.

    Args:
        pth (str): path to directory with sources

    Returns:
        (Image)
    """
    avatar_pth = pj(pth, "avatar.png")

    if not exists(avatar_pth):
        return None

    img = Image.open(avatar_pth)
    return img


def _readme_pth(pth):
    for name in ("README", "README.txt", "README.rst", "README.md"):
        readme_pth = pj(pth, name)
        if exists(readme_pth):
            return readme_pth
        readme_pth = pj(pth, name.lower())
        if exists(readme_pth):
            return readme_pth

    return None


def fetch_readme(pth):
    """Find readme file at the root of source dir.

    Args:
        pth (str): (source directory

    Returns:
        (str)
    """
    readme_pth = _readme_pth(pth)

    if readme_pth is None:
        return ""

    with open(readme_pth, 'r') as f:
        return f.read()


# def fetch_gallery(pid):
#     """Find all images in gallery associated to a project.
#
#     Args:
#         pid: (str) project id
#
#     Returns:
#         (list of (Image, str)): image, image_name
#     """
#     pth = source_pth(pid)
#     gallery_pth = pj(pth, "gallery")
#
#     if not exists(gallery_pth):
#         return []
#
#     imgs = []
#     for name in listdir(gallery_pth):
#         if splitext(name)[1] == ".png":
#             img = Image.open(pj(gallery_pth, name))
#             imgs.append((img, name))
#
#     return imgs
#
#
# def fetch_dependencies(pid):
#     """Analyse sources to extra project dependencies
#
#     Args:
#         pid: (str) project id
#
#     Returns:
#         (list of (str, str)): list of name, version
#     """
#     pth = source_pth(pid)
#     dep_pth = pj(pth, "requirements.txt")
#
#     if not exists(dep_pth):
#         return []
#
#     with open(dep_pth, 'r') as f:
#         txt = f.read()
#
#     reqs = []
#     for line in txt.splitlines():
#         line = line.strip()
#         if len(line) > 0 and not line.startswith("#"):
#             # TODO parse version
#             reqs.append((line, "none"))
#
#     return reqs
