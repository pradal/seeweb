from jinja2 import Markup
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.auth import Role
from seeweb.models.access import get_project, project_access_role
from seeweb.models.edit import create_project

from .tools import tabs, view_init


def register_new_project(request, session, uid):
    pid = request.params.get('project_id', "")
    if len(pid) == 0:
        request.session.flash("Enter a project id first", 'warning')
        return None

    pid = pid.lower().strip()
    if " " in pid:
        msg = "Project id ('%s') cannot have space" % pid
        request.session.flash(msg, 'warning')
        return None

    project = get_project(session, pid)
    if project is not None:
        if project.public:
            project_url = request.route_url('project_view_home',
                                            pid=pid)
            msg = "Project <a href='%s'>'%s'</a> already exists" % (project_url, pid)
            request.session.flash(Markup(msg), 'warning')
        else:
            msg = "Project '%s' already exists (private)" % pid
            request.session.flash(msg, 'warning')

        return None

    # create new project
    create_project(session, uid, pid)
    request.session.flash("New project %s created" % pid, 'success')
    return pid


@view_config(route_name='user_view_projects',
             renderer='templates/user/view_projects.jinja2')
def index(request):
    session = DBSession()
    user, view_params = view_init(request, session, 'projects')

    current_uid = view_params["current_uid"]

    if 'new_project' in request.params:
        pid = register_new_project(request, session, current_uid)
        if pid is not None:
            loc = request.route_url('project_edit_home', pid=pid)
            return HTTPFound(location=loc)

    projects = []
    for project in user.projects:
        role = project_access_role(session, project, current_uid)
        if role != Role.denied:
            projects.append((role, project))

    view_params["projects"] = projects

    allow_install = (current_uid == user.id)
    installed = []
    if allow_install:
        for project in user.installed:
            installed.append((Role.read, project))

    view_params["allow_install"] = allow_install
    view_params["installed"] = installed

    return view_params
