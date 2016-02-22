"""Set of functions to explore the content of a project i.e. its sources
"""
from glob import glob
from os.path import basename, dirname, exists
from os.path import join as pj


fac = dict()
for dpth in glob("%s/*/" % dirname(__file__)):
    if exists(pj(dpth, "thumbnail.py")):
        cat = basename(dirname(dpth))
        cmd = "from seeweb.project.content.%s.thumbnail import create_thumbnail" % cat
        code = compile(cmd, "<string>", 'exec')
        eval(code)
        fac[cat] = globals()['create_thumbnail']


def create_thumbnail(item, **kwds):
    """Create thumbnail associated to some content item.

    Args:
        item: (ContentItem)
        kwds: (dict of any) extra parameters

    Returns:
        Image or None if no thumbnail can be generated
    """
    if item.category not in fac:
        return None

    return fac[item.category](item, **kwds)
