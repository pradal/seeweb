"""Set of function used to fetch sources on remote hosts
"""
from urlparse import urlsplit

recognized_hosts = ["github", "pypi", "zenodo", "gforge", "local"]


def parse_vcs(url):
    """Find vcs associated to a given url

    Args:
        url: (str)

    Returns:
        (str) name of vcs
    """
    pth = urlsplit(url).path
    if pth.split(".")[-1] == "git":
        return "git"

    return "unknown"


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

    for name in recognized_hosts:
        if name in gr:
            return name

    return "unknown"


def host_src_url(project, hostname):
    """Generate normalized src url for the given host and project

    Args:
        project: (Project)
        hostname: (str) descriptor of a host name

    Returns:
        str
    """
    if hostname == 'github':
        return "https://github.com/%s/%s.git" % (project.owner, project.id)

    if hostname == 'pypi':
        return "https://pythonhosted.org/%s" % project.id

    return "unknown host: %s" % hostname
