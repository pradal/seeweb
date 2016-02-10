"""Extended io to fix some issues with default python implementations
"""
import os
import stat


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
