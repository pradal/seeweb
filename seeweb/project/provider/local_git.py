"""Locally clone git repository
"""
import os
from os.path import exists
from os.path import join as pj
from subprocess import call


def fetch_sources(src_url, dst):
    """Fetch sources located in src_url
    and copy them into a pid directory in dst.

    Args:
        src_url: (str) a valid url to fetch sources from
        dst: (str) a local path to copy files in

    Returns:
        (bool): whether sources have been retrieved or not
    """
    cwd = os.getcwd()
    repo_url = pj(cwd, src_url)
    if not exists(repo_url):
        return False

    # check dest
    if not exists(dst):
        os.mkdir(dst)

    os.chdir(dst)

    if not exists(".git"):
        call(["git", "init"])

    res = call(["git", "pull", repo_url])
    # print "res\n" * 10, res

    os.chdir(cwd)

    return True
