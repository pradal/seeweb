from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from seeweb.models.auth import Role
from seeweb.views.tools import get_current_uid

from .tools import get_project


@view_config(route_name='project_view_home_default', renderer='templates/project/view_home.jinja2')
@view_config(route_name='project_view_home', renderer='templates/project/view_home.jinja2')
def index(request):
    pid = request.matchdict['pid']

    project = get_project(request, pid)
    if project is None:
        request.session.flash("Project %s does not exists" % pid, 'warning')
        return HTTPFound(location=request.route_url('home'))

    current_uid = get_current_uid(request)
    role = project.access_role(current_uid)
    if role == Role.denied:
        request.session.flash("Access to %s not granted for you" % pid,
                              'warning')
        return HTTPFound(location=request.route_url('home'))

    return {"project": project,
            "tab": 'home',
            "allow_edit": role == Role.edit,
            "sections": ['description',
                         'gallery',
                         'comments',
                         'extra info']}
