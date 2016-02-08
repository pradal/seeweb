from os import listdir, remove, walk
from os.path import exists, splitext
from os.path import join as pj
from shutil import rmtree
from sys import argv


def clean(rep="."):
    """Thorough cleaning of all arborescence rooting at rep.

    Args:
        rep: (str) root directory to start the walk

    Returns:
        None
    """
    for name in ("build", "dist"):
        pth = pj(rep, name)
        if exists(pth):
            rmtree(pth)

    for root, dnames, fnames in walk(rep):
        # do not walk directories starting with "."
        for name in tuple(dnames):
            if "clean.no" in listdir(pj(root, name)):
                dnames.remove(name)
            elif name.startswith("."):
                dnames.remove(name)
            elif name == "__pycache__":
                rmtree(pj(root, name))
                dnames.remove(name)

        for name in fnames:
            if not name.startswith("."):
                if splitext(name)[1] in [".pyc", ".pyo"]:
                    remove(pj(root, name))


def clean_data():
    for root, dnames, fnames in walk("seeweb/data"):
        for name in fnames:
            if not name.startswith("."):
                if splitext(name)[1] in (".png",):
                    remove(pj(root, name))


def main():
    clean()

    if len(argv) > 1 and argv[1] == "all":
        clean_data()
