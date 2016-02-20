"""Set of functions to explore the content of a project i.e. its sources
"""
from glob import glob
from os.path import basename, dirname, exists
from os.path import join as pj

from seeweb.project.source import has_source, source_pth


fac = dict()
for dpth in glob("%s/*/" % dirname(__file__)):
    if exists(pj(dpth, "explore.py")):
        cat = basename(dirname(dpth))
        cmd = "from seeweb.project.content.%s.explore import explore_pth" % cat
        code = compile(cmd, "<string>", 'exec')
        eval(code)
        fac[cat] = globals()['explore_pth']


def explore_sources(session, project):
    """Explore source files associated to a project.

    Fill project content with all elements recognized
    by the platform.

    Args:
        session: (DBSession)
        project: (Project)

    Returns:
        None
    """
    if not has_source(project.id):
        print "nothing"
        return

    pth = source_pth(project.id).replace("\\", "/")

    project.clear_content(session)
    for category, explore_pth in fac.items():
        explore_pth(session, pth, project)
