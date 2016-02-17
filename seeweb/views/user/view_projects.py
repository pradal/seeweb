from jinja2 import Markup
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.auth import Role
from seeweb.models.project import Project

from .commons import view_init


def register_new_project(request, session, uid):
    """Create a new project from information in the view.

    Args:
        request: (request)
        session: (DBSession)
        uid: (str) id of user future owner of the project.

    Returns:
        (None|str): None if creation failed, pid if success
    """
    pid = request.params.get('project_id', "")
    if len(pid) == 0:
        request.session.flash("Enter a project id first", 'warning')
        return None

    pid = pid.lower().strip()
    if " " in pid:
        msg = "Project id ('%s') cannot have space" % pid
        request.session.flash(msg, 'warning')
        return None

    project = Project.get(session, pid)
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
    Project.create(session, uid, pid)
    request.session.flash("New project %s created" % pid, 'success')
    return pid


@view_config(route_name='user_view_projects',
             renderer='templates/user/view_projects.jinja2')
def view(request):
    session = DBSession()
    user, view_params = view_init(request, session, 'projects')

    if 'new_project' in request.params:
        pid = register_new_project(request,
                                   session,
                                   request.unauthenticated_userid)
        if pid is not None:
            loc = request.route_url('project_edit_home', pid=pid)
            return HTTPFound(location=loc)

    projects = []
    for project in user.projects:
        role = project.access_role(session,
                                   request.unauthenticated_userid)
        if role != Role.denied:
            projects.append((Role.to_str(role), project))

    view_params["projects"] = projects

    installed_projects = []
    for installed in user.installed:
        project = Project.get(session, installed.project)
        installed_projects.append((installed.date.strftime("%Y-%m-%d"),
                                   project))

    view_params["installed_projects"] = installed_projects

    return view_params
