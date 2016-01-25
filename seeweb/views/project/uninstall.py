from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.access import get_project, get_user, project_access_role
from seeweb.models.auth import Role
from seeweb.models.edit import uninstall_project
from seeweb.playground import workspace


@view_config(route_name='project_uninstall',
             renderer='templates/project/uninstall.jinja2')
def view(request):
    session = DBSession()
    pid = request.matchdict['pid']

    if 'cancel' in request.params:
        # back to project page
        loc = request.route_url('project_view_home', pid=pid)
        return HTTPFound(location=loc)

    project = get_project(session, pid)
    if project is None:
        request.session.flash("Project %s does not exists" % pid, 'warning')
        raise HTTPFound(location=request.route_url('home'))

    current_uid = request.unauthenticated_userid
    role = project_access_role(session, project, current_uid)
    if role == Role.denied:
        request.session.flash("Access to %s not granted for you" % pid,
                              'warning')
        raise HTTPFound(location=request.route_url('home'))

    if 'validate' in request.params:
        # uninstall project
        user = get_user(session, current_uid)
        if user is None:
            loc = request.route_url('project_view_home', pid=project.id)
            return HTTPFound(location=loc)

        uninstall_project(session, user, project)
        if workspace.has_workspace(user.id):
            try:
                workspace.uninstall_project(user.id, project.id)
            except UserWarning:
                request.session.flash("Unable to uninstall %s" % pid,
                                      'warning')

        loc = request.route_url('user_view_projects', uid=current_uid)
        return HTTPFound(location=loc)

    return {'project': project}

