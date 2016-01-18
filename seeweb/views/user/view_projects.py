from jinja2 import Markup
from pyramid.view import view_config

from seeweb.models.auth import Role
from seeweb.models.access import get_project, project_access_role
from seeweb.models.edit import create_project

from .tools import tabs, view_init


@view_config(route_name='user_view_projects', renderer='templates/user/view_projects.jinja2')
def index(request):
    user, current_uid, allow_edit = view_init(request)

    if 'new_project' in request.params:
        pid = request.params.get('project_id', "")
        if len(pid) == 0:
            request.session.flash("Enter a project id first", 'warning')
        else:
            pid = pid.lower().strip()
            if " " in pid:
                request.session.flash("Project id ('%s') cannot have space" % pid, 'warning')
            else:
                project = get_project(pid)
                if project is not None:
                    if project.public:
                        project_url = request.route_url('project_view_home', pid=pid)
                        msg = "Project <a href='%s'>'%s'</a> already exists" % (project_url, pid)
                        request.session.flash(Markup(msg), 'warning')
                    else:
                        request.session.flash("Project '%s' already exists (private)" % pid, 'warning')
                else:
                    # create new project
                    create_project(current_uid, pid)
                    request.session.flash("New project %s created" % pid, 'success')

    projects = []
    for project in user.projects:
        role = project_access_role(project, current_uid)
        if role != Role.denied:
            projects.append((role, project))

    return {"user": user,
            "tabs": tabs,
            "tab": 'projects',
            "allow_edit": allow_edit,
            "projects": projects}
