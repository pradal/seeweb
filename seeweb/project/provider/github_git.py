"""Clone git repository hosted on github
"""
import os
from os.path import exists
from subprocess import call
from urlparse import urlsplit


def parse_url(url):
    """Parse a repository url to extract owner and project name

    Args:
        url: (str) url of project repository on github

    Returns:
        (str, str): owner, project name
    """
    url = urlsplit(url)
    if url.netloc != "github.com":
        return None, None

    gr = url.path.split("/")
    if len(gr) != 3:
        return None, None

    dmy, owner, name = gr

    return owner, name.split(".")[0]


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
