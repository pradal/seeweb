"""Set of function to explore sources of a project and retrieve
relevant items.
"""

from ConfigParser import ConfigParser
import json
from os import listdir, walk
from os.path import exists, splitext
from os.path import join as pj
from PIL import Image

from .source import source_pth


def find_notebooks(pid):
    """Walks all sources and return a list of notebooks.

    Args:
        pid: (str) id of project to scan

    Returns:
        (list of str)
    """
    pth = source_pth(pid).replace("\\", "/")

    n = len(pth)
    notebooks = []
    for root, dirnames, filenames in walk(pth):
        # avoid hidden directories
        for i in range(len(dirnames) - 1, -1, -1):
            if dirnames[i].startswith("."):
                del dirnames[i]

        # find notebooks
        for name in filenames:
            if splitext(name)[1] == ".ipynb":
                dname = root.replace("\\", "/")[n:]
                notebooks.append((dname, name))

    return notebooks


def find_executables(pid):
    """Find all console_scripts entry points in a project.

    Args:
        pid: (str) id of project to scan

    Returns:
        (list of str)
    """
    pth = source_pth(pid)

    setup_pth = pj(pth, "setup.py")
    if not exists(setup_pth):
        return []

    egg_pth = pj(pth, "src", "%s.egg-info" % pid)
    if not exists(egg_pth):
        return []

    cf = ConfigParser()
    cf.read(pj(egg_pth, "entry_points.txt"))
    if cf.has_section('console_scripts'):
        eps = cf.items('console_scripts')
    else:
        eps = []

    return eps


def find_workflow_nodes(pid):
    """Find all defined workflow nodes in the project.

    Args:
        pid: (str) project id

    Returns:
        (list of Node): list of defined nodes
    """
    pth = source_pth(pid)

    plugin_pth = pj(pth, "src", "%s_plugin" % pid)
    if not exists(plugin_pth):
        return []

    nodes = []
    for root, dirnames, filenames in walk(plugin_pth):
        # avoid hidden directories
        for i in range(len(dirnames) - 1, -1, -1):
            if dirnames[i].startswith("."):
                del dirnames[i]

        # find notebooks
        for name in filenames:
            if splitext(name)[1] == ".json":
                with open(pj(root, name), 'r') as f:
                    node_def = json.load(f)
                    if node_def["category"] == "oanode":
                        nodes.append(node_def)

    return nodes


def fetch_avatar(pid):
    """Find avatar file at the root of source dir.

    Args:
        pid: (str) project id

    Returns:
        (Image)
    """
    pth = source_pth(pid)
    avatar_pth = pj(pth, "avatar.png")

    if not exists(avatar_pth):
        return None

    img = Image.open(avatar_pth)
    return img


def _readme_pth(pth):
    for name in ("readme.rst", "readme.txt", "README", "README.txt"):
        readme_pth = pj(pth, name)
        if exists(readme_pth):
            return readme_pth

    return None


def fetch_readme(pid):
    """Find readme file at the root of source dir.

    Args:
        pid: (str) project id

    Returns:
        (Image)
    """
    readme_pth = _readme_pth(source_pth(pid))

    if readme_pth is None:
        return ""

    with open(readme_pth, 'r') as f:
        return f.read()


def fetch_gallery(pid):
    """Find all images in gallery associated to a project.

    Args:
        pid: (str) project id

    Returns:
        (list of (Image, str)): image, image_name
    """
    pth = source_pth(pid)
    gallery_pth = pj(pth, "gallery")

    if not exists(gallery_pth):
        return []

    imgs = []
    for name in listdir(gallery_pth):
        if splitext(name)[1] == ".png":
            img = Image.open(pj(gallery_pth, name))
            imgs.append((img, name))

    return imgs


def fetch_dependencies(pid):
    """Analyse sources to extra project dependencies

    Args:
        pid: (str) project id

    Returns:
        (list of (str, str)): list of name, version
    """
    pth = source_pth(pid)
    dep_pth = pj(pth, "requirements.txt")

    if not exists(dep_pth):
        return []

    with open(dep_pth, 'r') as f:
        txt = f.read()

    reqs = []
    for line in txt.splitlines():
        line = line.strip()
        if len(line) > 0 and not line.startswith("#"):
            # TODO parse version
            reqs.append((line, "none"))

    return reqs
