"""Clone git repository hosted on github
"""
import os
from os.path import exists, normpath
from subprocess import call


def fetch_sources(repo_url, dst):
    """Fetch sources located in src_url
    and copy them into a pid directory in dst.

    Args:
        repo_url: (str) a valid url to fetch sources from
        dst: (str) a local path to copy files in

    Returns:
        (bool): whether sources have been retrieved or not
    """
    cwd = os.getcwd()
    os.chdir(dst)

    if not exists(".git"):
        call(["git", "init"])

    cmd = "git pull %s" % repo_url
    print "cmd:", cmd, "\n" * 10

    res = 1
    try:
        res = call(cmd, shell=True)
    finally:
        os.chdir(cwd)

    return res == 0
