"""Set of function used to fetch sources on remote hosts
"""
from os import mkdir
from os.path import dirname, exists, join
from urlparse import urlsplit

from .provider import local_git

recognized_hosts = {"github": "github.com",
                    "pypi": "pypi.python.org",
                    "zenodo": "zenodo.org",
                    "gforge": "gforge.inria.fr"}


def source_pth(pid):
    """Return a path to the source dir associated to a given project.

    Args:
        pid: (str) project id

    Returns:
        (str): path, may miss last dirname
    """
    root = dirname(dirname(dirname(dirname(__file__))))
    return join(root, "see_repo", pid)


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

    ref_url = url.netloc.lower()

    for name, host_url in recognized_hosts.items():
        if host_url in ref_url:
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
        return "https://pypi.python.org/pypi/%s" % project.id

    if hostname == 'zenodo':
        return "https://zenodo.org/record/%s" % project.id

    if hostname == 'gforge':
        return "https://gforge.inria.fr/projects/%s" % project.id

    return "unknown host: %s" % hostname


def fetch_sources(project):
    """Fetch source for a given project according to project.src_url

    Args:
        project: (Project)

    Returns:
        (bool): whether fetch has been successful
    """
    vcs = parse_vcs(project.src_url)
    if vcs != "git":
        return False

    pth = source_pth(project.id)
    if not exists(pth):
        mkdir(pth)

    host = parse_hostname(project.src_url)
    if host == 'github':
        return False

    if host == 'local':
        return local_git.fetch_sources(project.src_url, pth)

    return False
