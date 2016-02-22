"""Clone git repository hosted on github
"""


def project_default_url(project):
    """Generate the default url of the project for this provider

    Args:
        project: (Project)

    Returns:
        (str): url where to find the project
    """
    return "https://pypi.python.org/pypi/%s" % project.id


def parse_url(url):
    """Parse a repository url to extract project name

    Args:
        url: (urlsplit) url of project repository on github

    Returns:
        (str): project name or None if url not recognized
    """
    if url.netloc != "pypi.python.org":
        return None

    gr = url.path.split("/")
    if len(gr) != 3:
        return None

    dmy, pypi, name = gr

    return name


def fetch_sources(repo_url, dst):
    """Fetch sources located in src_url
    and copy them into a pid directory in dst.

    Args:
        repo_url: (str) a valid url to fetch sources from
        dst: (str) a local path to copy files in

    Returns:
        (bool): whether sources have been retrieved or not
    """
    del repo_url
    del dst
    return False
