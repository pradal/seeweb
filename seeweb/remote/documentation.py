"""Set of function used to fetch documentation on remote hosts
"""
from urlparse import urlsplit


def parse_hostname(url):
    """Find host name associated to a given url

    Args:
        url: (str)

    Returns:
        (str) name of host
    """
    netloc = urlsplit(url).netloc
    gr = netloc.split(".")
    if gr[-2] == "readthedocs":
        return "readthedocs"

    return "unknown"
