"""Default API for source providers
"""
import os
from os.path import exists


def project_default_url(project):
    """Generate the default url of the project for this provider

    Args:
        project: (Project)

    Returns:
        (str): url where to find the project
    """
    del project
    raise NotImplementedError


def parse_url(url):
    """Parse a repository url to extract project name

    Args:
        url: (urlsplit) url of project repository

    Returns:
        (str): project name
    """
    del url
    raise NotImplementedError


def fetch_sources(src_url, dst):
    """Fetch sources located in src_url
    and copy them into a pid directory in dst.

    Args:
        src_url: (str) a valid url to fetch sources from
        dst: (str) a local path to copy files in

    Returns:
        (bool): whether sources have been retrieved or not
    """
    del src_url

    if not exists(dst):
        os.mkdir(dst)

    return True
