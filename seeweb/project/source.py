"""Set of function used to fetch sources on remote hosts
"""
from glob import glob
from os import mkdir, remove
from os.path import basename, dirname, exists, splitext
from os.path import join as pj
from urlparse import urlsplit
from zipfile import BadZipfile, ZipFile

from seeweb.io import rmtree

fac = dict()
for pth in glob("%s/src_provider/*.py" % dirname(__file__)):
    fname = basename(pth)
    if fname not in("__init__.py", "default.py"):
        pname = splitext(fname)[0]
        cmd = "from seeweb.project.src_provider import %s as provider" % pname
        code = compile(cmd, "<string>", 'exec')
        eval(code)
        fac[pname] = globals()['provider']

recognized_hosts = fac.keys()


def source_pth(pid):
    """Return a path to the source dir associated to a given project.

    Args:
        pid: (str) project id

    Returns:
        (str): path, may miss last dirname
    """
    root = dirname(dirname(dirname(dirname(__file__))))
    return pj(root, "see_repo", pid)


def has_source(pid):
    """Check if the project has some local sources.

    Args:
        pid: (str) project id

    Returns:
        (bool)
    """
    return exists(source_pth(pid))


def delete_source(pid):
    """Wipe the content of the source folder.

    Args:
        pid: (str) project id

    Returns:
        (None)
    """
    if has_source(pid):
        try:
            rmtree(source_pth(pid))
        except OSError:
            print "unable to destroy %s" % source_pth(pid), "\n" * 10


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


def parse_url(url, hostname):
    """Parse a repository url to extract owner and project name

    Args:
        url: (urlsplit) url of project repository
        hostname: (str) remote host name

    Returns:
        (str, str): owner, project name
    """
    if hostname in fac:
        url = urlsplit(url)
        return fac[hostname].parse_url(url)

    return None


def host_src_url(project, hostname):
    """Generate normalized src url for the given host and project

    Args:
        project: (Project)
        hostname: (str) descriptor of a host name

    Returns:
        str
    """
    if hostname in fac:
        return fac[hostname].project_default_url(project)

    return "unknown host: %s" % hostname


def fetch_sources(project):
    """Fetch source for a given project according to project.src_url

    Args:
        project: (Project)

    Returns:
        (bool): whether fetch has been successful
    """
    if project.src_url == "":
        return False

    hostname = parse_hostname(project.src_url)
    if hostname == "unknown":
        return False

    pth = source_pth(project.id)
    if not exists(pth):
        mkdir(pth)

    return fac[hostname].fetch_sources(project.src_url, pth)


def upload_src_file(field_storage, pid):
    """Write the content of field_storage in the src space.

    Args:
        field_storage: (FieldStorage) html structure
        pid: (str) project id

    Returns:
        (str) name of file written
    """
    pth = source_pth(pid)
    if not exists(pth):
        mkdir(pth)

    file_name = str(field_storage.filename)
    input_file = field_storage.file
    input_file.seek(0)
    with open(pj(pth, file_name), 'wb') as f:
        f.write(input_file.read())

    # try to unpack zip files
    try:
        with ZipFile(pj(pth, file_name), 'r') as myzip:
            myzip.extractall(pth)

        remove(pj(pth, file_name))
    except BadZipfile:
        # not a zip file, do nothing
        pass

    return file_name
