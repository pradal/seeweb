from os.path import basename, exists, splitext
from pyramid.view import view_config
from urlparse import urlsplit

from seeweb.models import DBSession
from seeweb.model_access import get_user
# from seeweb.playground.workspace import has_workspace
from seeweb.project.source import parse_vcs, parse_hostname, source_pth
from seeweb.project.explore_sources import find_executables, find_notebooks

from .commons import view_init


@view_config(route_name='project_view_source',
             renderer='templates/project/view_source.jinja2')
def view(request):
    session = DBSession()
    project, view_params = view_init(request, session, 'source')

    if len(project.src_url) > 0:
        vcs = parse_vcs(project.src_url)
        hostname = parse_hostname(project.src_url)
    else:
        vcs = ""
        hostname = ""

    view_params["vcs"] = vcs
    view_params["hostname"] = hostname

    # explore sources
    for name in ["notebooks", "executables"]:
        view_params[name] = []

    src_pth = source_pth(project.id)
    if exists(src_pth):
        view_params["notebooks"] = find_notebooks(src_pth)
        view_params["executables"] = find_executables(project.id)

    playground = False
    # user = get_user(session, view_params["current_uid"])
    # view_params["user"] = user
    # if user is not None and project in user.installed:
    #     if has_workspace(user.id):
    #         playground = True

    view_params["playground"] = playground

    return view_params
