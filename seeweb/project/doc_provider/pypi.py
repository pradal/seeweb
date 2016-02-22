"""Default API for documentation providers
"""
from bs4 import BeautifulSoup
import urllib2
from urllib2 import HTTPError
from urlparse import urlsplit, urlunsplit


def project_default_url(project):
    """Generate the default url of the project for this provider

    Args:
        project: (Project)

    Returns:
        (str): url where to find the project documentation
    """
    return "https://pythonhosted.org/%s/" % project.id


def parse_url(url):
    """Parse a repository url to extract project name

    Args:
        url: (urlsplit) url of project repository

    Returns:
        (str): project name
    """
    if url.netloc != "pythonhosted.org":
        return None

    gr = url.path.split("/")
    if len(gr) != 3:
        return None

    dmy, name, dmy = gr

    return name


def fetch_documentation(url, pid):
    """Fetch documentation home page.

    Args:
        url: (str) a valid url to fetch documentation from
        pid: (str) project id

    Returns:
        (str): home page of documentation or None
    """
    raise NotImplementedError
