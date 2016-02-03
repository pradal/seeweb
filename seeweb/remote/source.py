"""Set of function used to fetch sources on remote hosts
"""
from urlparse import urlsplit


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
    netloc = urlsplit(url).netloc
    if len(netloc) == 0:
        return "local"

    gr = netloc.split(".")
    if gr[-2] == "github":
        return "github"

    return "unknown"
