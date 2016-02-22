"""Set of function used to fetch documentation on remote hosts
"""
from glob import glob
from os.path import basename, dirname, splitext
from urlparse import urlsplit

fac = dict()
for pth in glob("%s/doc_provider/*.py" % dirname(__file__)):
    fname = basename(pth)
    if fname not in("__init__.py", "default.py"):
        pname = splitext(fname)[0]
        cmd = "from seeweb.project.doc_provider import %s as provider" % pname
        code = compile(cmd, "<string>", 'exec')
        eval(code)
        fac[pname] = globals()['provider']

recognized_hosts = fac.keys()


def parse_hostname(url):
    """Find host name associated to a given url

    Args:
        url: (str)

    Returns:
        (str) name of host
    """
    url = urlsplit(url)
    for pname, provider in fac.items():
        if provider.parse_url(url) is not None:
            return pname

    return "unknown"


def host_doc_url(project, hostname):
    """Generate normalized doc url for the given host and project

    Args:
        project: (Project)
        hostname: (str) descriptor of a host name

    Returns:
        str
    """
    if hostname in fac:
        return fac[hostname].project_default_url(project)

    return "unknown host: %s" % hostname


def fetch_documentation(url, pid):
    """Fetch documentation home page.

    Args:
        url: (str) a valid url to fetch documentation from
        pid: (str) project id

    Returns:
        (str): home page of documentation or None
    """
    if url == "":
        return None

    hostname = parse_hostname(url)
    if hostname == "unknown":
        return None

    return fac[hostname].fetch_documentation(url, pid)
