from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from seeweb.views.tools import get_current_uid

from .tools import get_project


@view_config(route_name='project_home', renderer='templates/project/home.jinja2')
def index(request):
    uid = request.matchdict['uid']
    pid = request.matchdict['pid']

    project = get_project(request, uid, pid)

    current_uid = get_current_uid(request)
    if (not project.public) and (project.owner != current_uid):
        request.session.flash("Access to %s not granted for you" % pid,
                              'warning')
        return HTTPFound(location=request.route_url('home'))

    return {"project": project, "allow_edit": current_uid == project.owner}
