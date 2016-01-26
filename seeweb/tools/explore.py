import ast
from ast import parse
from ConfigParser import ConfigParser
from os import walk
from os.path import exists, splitext
from os.path import join as pj

from seeweb.views.tools import source_pth


def find_notebooks(pth):
    """Walks all sources and return a list of notebooks.
    """
    pth = pth.replace("\\", "/")
    n = len(pth)
    notebooks = []
    for root, dirnames, filenames in walk(pth):
        # avoid hidden directories
        for i in range(len(dirnames) - 1, -1, -1):
            if dirnames[i].startswith("."):
                del dirnames[i]

        # fidn notebooks
        for name in filenames:
            if splitext(name)[1] == ".ipynb":
                dname = root.replace("\\", "/")[n:]
                notebooks.append((dname, name))

    return notebooks


def parse_console_script(elm):
    """Construct a list of console scripts.
    """
    exename, exepth = elm.split("=")
    # TODO
    # find associated description as docstring
    # of refered function
    descr = "No description found yet (TODO)"

    return exename.strip(), descr


def parse_console_scripts(elms):
    """Construct a list of console scripts.
    """
    executables = []
    for descr in elms:
        exename, exepth = descr.split("=")
        # TODO
        # find associated description as docstring
        # of refered function
        descr = "No description found yet (TODO)"
        executables.append((exename.strip(), descr))

    return executables


def parse_entry_points(eps):
    for i, key in enumerate(eps.keys):
        if key.s == 'console_scripts':
            scripts = eps.values[i]
            return parse_console_scripts([it.s for it in scripts.elts])


def parse_setup(pth):
    setup_pth = pj(pth, "setup.py")
    with open(setup_pth, 'r') as f:
        tree = parse(f.read(), "setup.py")

    # find setup function
    for item in tree.body:
        if isinstance(item, ast.Expr):
            if item.col_offset == 0 and isinstance(item.value, ast.Call):
                ca = item.value
                if ca.func.id == "setup":
                    for kwd in ca.keywords:
                        if kwd.arg == "entry_points":
                            return parse_entry_points(kwd.value)


def find_executables(pid):
    """Find all console_scripts entry points in a project
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