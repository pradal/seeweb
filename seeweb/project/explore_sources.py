"""Set of function to explore sources of a project and retrieve
relevant items.
"""

from ConfigParser import ConfigParser
from os import walk
from os.path import exists, splitext
from os.path import join as pj

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
