"""Set of function used to fetch documentation on remote hosts
"""
from bs4 import BeautifulSoup
import urllib2
from urllib2 import HTTPError
from urlparse import urlsplit, urlunsplit

recognized_hosts = {"readthedocs": "readthedocs.org",
                    "pypi": "pythonhosted.org"}


def parse_hostname(url):
    """Find host name associated to a given url

    Args:
        url: (str)

    Returns:
        (str) name of host
    """
    url = urlsplit(url)
    if len(url.netloc) == 0:
        if "/" in url.path:
            return "local"
        else:
            return "unknown"

    gr = [v.lower() for v in url.netloc.split(".")]
    if len(gr) < 2:
        return "unknown"

    hurl = "%s.%s" % (gr[-2], gr[-1])

    for host, host_url in recognized_hosts.items():
        if hurl == host_url:
            return host

    return "unknown"


def host_doc_url(project, hostname):
    """Generate normalized doc url for the given host and project

    Args:
        project: (Project)
        hostname: (str) descriptor of a host name

    Returns:
        str
    """
    if hostname == 'readthedocs':
        return "https://%s.readthedocs.org/en/latest/" % project.id

    if hostname == 'pypi':
        return "https://pythonhosted.org/%s" % project.id

    return "unknown host: %s" % hostname


def fetch_documentation(url, pid):
    """Try to fetch documentation from given url
    return html home page for doc
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
