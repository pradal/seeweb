from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.access import get_team, get_user
from seeweb.models.edit import create_user
from seeweb.playground.workspace import create_workspace

from .tools import log_user


@view_config(route_name='user_register', renderer='templates/register.jinja2')
def index(request):
    if "ok" in request.params:
        session = DBSession()

        # check all fields are correct
        uid = request.params["user_id"]
        if len(uid) == 0:  # test user_id validity
            request.session.flash("No user id given", 'warning')
            return HTTPFound(location=request.route_url('user_register'))

        name = request.params["user_name"]
        if len(name) == 0:  # test name validity
            request.session.flash("No name given", 'warning')
            return HTTPFound(location=request.route_url('user_register'))

        email = request.params["user_email"]
        if len(email) == 0:  # test name validity
            request.session.flash("No email given", 'warning')
            return HTTPFound(location=request.route_url('user_register'))

        # check user does not exist already
        # as a user
        user = get_user(session, uid)
        if user is not None:
            request.session.flash("User %s already exists" % uid, 'warning')
            return HTTPFound(location=request.route_url('user_register'))

        # as a team
        team = get_team(session, uid)
        if team is not None:
            msg = "User %s already exists as a team name" % uid
            request.session.flash(msg, 'warning')
            return HTTPFound(location=request.route_url('user_register'))

        # register new user
        create_user(session, uid, name, email)
        return log_user(request, uid, 'edit_after' in request.params)

    else:
        return {}
