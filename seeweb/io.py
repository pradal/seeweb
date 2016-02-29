"""Extended io to fix some issues with default python implementations
"""
from fnmatch import fnmatch
import os
import stat


def find_files(root_pth, patterns):
    """Explore recursively pth to find files with the given patterns.

    Notes: Do not process hidden directories (i.e. starting with '.')

    Args:
        root_pth: (str) root dir to start exploring
        patterns: (list of str) list of patterns to consider:
                   e.g. ['*.png', '*.gif']

    Returns:
        (str, str)
    """
    for root, dir_names, file_names in os.walk(root_pth):
        # avoid hidden directories
        for i in range(len(dir_names) - 1, -1, -1):
            if dir_names[i].startswith("."):
                del dir_names[i]

        # find recognized content items
        for fname in file_names:
            if any(fnmatch(fname, pat) for pat in patterns):
                pth = os.path.join(root, fname)
                yield pth, fname


def rmtree(top):
    """Remove a top directory even if not empty

    Args:
        top: (str) path to directory

    Returns:
        None
    """
    for root, dirs, files in os.walk(top, topdown=False):
        for name in files:
            filename = os.path.join(root, name)
            os.chmod(filename, stat.S_IWUSR)
            os.remove(filename)
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(top)
