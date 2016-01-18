from jinja2 import Markup
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
    else:
        pid = pid.lower().strip()
        if " " in pid:
            msg = "Project id ('%s') cannot have space" % pid
            request.session.flash(msg, 'warning')
        else:
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
            else:
                # create new project
                create_project(session, uid, pid)
                request.session.flash("New project %s created" % pid, 'success')


@view_config(route_name='user_view_projects',
             renderer='templates/user/view_projects.jinja2')
def index(request):
    session = DBSession()
    user, current_uid, allow_edit = view_init(request, session)

    if 'new_project' in request.params:
        register_new_project(request, session, current_uid)

    projects = []
    for project in user.projects:
        role = project_access_role(session, project, current_uid)
        if role != Role.denied:
            projects.append((role, project))

    return {"user": user,
            "tabs": tabs,
            "tab": 'projects',
            "allow_edit": allow_edit,
            "projects": projects}
