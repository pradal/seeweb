"""Clone git repository hosted on github
"""
import os
from os.path import exists
from subprocess import call
from urlparse import urlsplit


def project_default_url(project):
    """Generate the default url of the project for this provider

    Args:
        project: (Project)

    Returns:
        (str): url where to find the project
    """
    return "https://github.com/%s/%s.git" % (project.owner, project.id)


def parse_url(url):
    """Parse a repository url to extract project name

    Args:
        url: (urlsplit) url of project repository on github

    Returns:
        (str): project name or None if url not recognized
    """
    if url.netloc != "github.com":
        return None

    gr = url.path.split("/")
    if len(gr) != 3:
        return None

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
