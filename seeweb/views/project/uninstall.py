from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.user import User
from seeweb.model_edit import uninstall_project

from .commons import install_init


@view_config(route_name='project_uninstall',
             renderer='templates/project/uninstall.jinja2')
def view(request):
    session = DBSession()
    project, view_params = install_init(request, session)

    if 'validate' in request.params:
        # uninstall project
        user = User.get(session, request.unauthenticated_userid)
        if user is None:
            loc = request.route_url('project_view_home', pid=project.id)
            return HTTPFound(location=loc)

        uninstall_project(session, user, project)

        loc = request.route_url('user_view_projects',
                                uid=request.unauthenticated_userid)
        return HTTPFound(location=loc)

    return view_params

