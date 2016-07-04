"""Extended io to fix some issues with default python implementations
"""
import json
from jsonschema import validate, ValidationError
from fnmatch import fnmatch
import os
from os.path import abspath, dirname, exists
from os.path import join as pj
from random import sample
import stat


def temp_pth():
    """Return a path to the temporary directory.

    Returns:
        (str): path
    """
    root = dirname(dirname(dirname(abspath(__file__))))
    return pj(root, "see_repo")


def random_name():
    """Generates a random 6 letters long name.

    Returns:
        (str)
    """
    return "".join(sample("abcdefghijklmnopqrstuvwxyz", 6))


def find_files(root_pth, patterns):
    """Explore recursively pth to find files with the given patterns.

    Notes: Do not process hidden directories (i.e. starting with '.')

    Args:
        root_pth: (str) root dir to start exploring
        patterns: (list of str) list of file name patterns to consider:
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


def find_definitions(root_pth, schema, patterns):
    """Explore recursively pth to find files with the given patterns.

    Notes: Do not process hidden directories (i.e. starting with '.')

    Args:
        root_pth: (str) root dir to start exploring
        schema: (dict) json schema defining an object type
        patterns: (list of str) list of file name patterns to consider:
                   e.g. ['*.png', '*.gif']

    Returns:
        (str, str)
    """
    for pth, fname in find_files(root_pth, patterns):
        with open(pth, 'r') as f:
            idef = json.load(f)
            try:
                validate(idef, schema)
                yield pth, fname, idef
            except ValidationError:
                print "%s not a valid object" % pth


def load_schema(here):
    """Load a json schema definition

    Args:
        here: (str) path to python file

    Returns:
        dict
    """
    with open(os.path.join(os.path.dirname(here), "schema.json"), 'r') as f:
        return json.load(f)


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


def upload_file(field_storage):
    """Write the content of field_storage in a temporary space.

    Args:
        field_storage: (FieldStorage) html structure

    Returns:
        (str, str) path of file written (dirname, filename)
    """
    pth = pj(temp_pth(), random_name())
    while exists(pth):
        pth = pj(temp_pth(), random_name())

    os.mkdir(pth)

    file_pth = pj(pth, str(field_storage.filename))
    input_file = field_storage.file
    input_file.seek(0)
    with open(file_pth, 'wb') as f:
        f.write(input_file.read())

    return file_pth
