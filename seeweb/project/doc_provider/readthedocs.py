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
    return "https://%s.readthedocs.org/en/latest/" % project.id


def parse_url(url):
    """Parse a repository url to extract project name

    Args:
        url: (urlsplit) url of project repository

    Returns:
        (str): project name
    """
    if "readthedocs.org" not in url.netloc:
        return None

    gr = url.netloc.split(".")
    if len(gr) != 3:
        return None

    name, readthedocs, org = gr

    return name


def fetch_documentation(url, pid):
    """Fetch documentation home page.

    Args:
        url: (str) a valid url to fetch documentation from
        pid: (str) project id

    Returns:
        (str): home page of documentation or None
    """
    try:
        scheme = urlsplit(url).scheme
        netloc = "%s.readthedocs.org/en/latest" % pid

        response = urllib2.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html, "html.parser")
        section = soup.find('div', {'class': 'section'})
        if section is None:
            return None

        for link in section.find_all('a'):
            url = urlsplit(link["href"])
            if url.netloc == "":
                link["href"] = urlunsplit((scheme, netloc) + url[2:])

        txt = section.prettify()
        return txt
    except HTTPError:
        return None
