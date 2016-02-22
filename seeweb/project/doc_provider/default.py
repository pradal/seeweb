"""Default API for documentation providers
"""


def project_default_url(project):
    """Generate the default url of the project for this provider

    Args:
        project: (Project)

    Returns:
        (str): url where to find the project documentation
    """
    del project
    raise NotImplementedError


def parse_url(url):
    """Parse a repository url to extract project name

    Args:
        url: (urlsplit) url of project repository

    Returns:
        (str): project name
    """
    del url
    raise NotImplementedError


def fetch_documentation(url, pid):
    """Fetch documentation home page.

    Args:
        url: (str) a valid url to fetch documentation from
        pid: (str) project id

    Returns:
        (str): home page of documentation or None
    """
    del url
    del pid
    raise NotImplementedError
