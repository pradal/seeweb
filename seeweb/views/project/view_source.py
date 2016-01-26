from os.path import exists
from pyramid.view import view_config
from urlparse import urlsplit

from seeweb.models import DBSession
from seeweb.models.access import get_user
from seeweb.playground.workspace import has_workspace
from seeweb.tools.explore import find_executables, find_notebooks
from seeweb.views.tools import source_pth

from .tools import view_init


@view_config(route_name='project_view_source',
             renderer='templates/project/view_source.jinja2')
def index(request):
    session = DBSession()
    project, view_params = view_init(request, session, 'source')

    hostname = ""
    if len(project.src_url) > 0:
        url = urlsplit(project.src_url)
        hostname = url.hostname

    if hostname is None or len(hostname) == 0:
        hostname = "src hostname"

    view_params["hostname"] = hostname

    # explore sources
    for name in ["notebooks", "executables"]:
        view_params[name] = []

    src_pth = source_pth(project.id)
    if exists(src_pth):
        view_params["notebooks"] = find_notebooks(src_pth)
        view_params["executables"] = find_executables(src_pth)

    playground = False
    user = get_user(session, view_params["current_uid"])
    view_params["user"] = user
    if user is not None and project in user.installed:
        if has_workspace(user.id):
            playground = True

    view_params["playground"] = playground

    return view_params
