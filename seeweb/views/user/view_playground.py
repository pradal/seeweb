from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.playground.workspace import (create_workspace,
                                         has_workspace,
                                         install_project,
                                         remove_workspace)

from .tools import view_init


@view_config(route_name='user_view_playground',
             renderer='templates/user/view_playground.jinja2')
def index(request):
    session = DBSession()
    user, view_params = view_init(request, session, 'playground')

    if not view_params["allow_edit"]:
        msg = "Access to %s playground not granted for you" % user.id
        request.session.flash(msg, 'warning')
        raise HTTPFound(location=request.route_url('home'))

    if "create" in request.params:
        if not has_workspace(user.id):
            create_workspace(user.id)
            for project in user.installed:
                try:
                    install_project(user.id, project.id)
                except UserWarning:
                    msg = "Unable to install %s" % project.id
                    request.session.flash(msg, 'warning')

    if "clear" in request.params:
        if has_workspace(user.id):
            remove_workspace(user.id)

    return view_params
