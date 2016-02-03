"""Set of function used to fetch documentation on remote hosts
"""
from urlparse import urlsplit

recognized_hosts = ["readthedocs", "pypi", "local"]


def parse_hostname(url):
    """Find host name associated to a given url

    Args:
        url: (str)

    Returns:
        (str) name of host
    """
    netloc = urlsplit(url).netloc
    gr = [v.lower() for v in netloc.split(".")]

    for name in recognized_hosts:
        if name in gr:
            return name

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
