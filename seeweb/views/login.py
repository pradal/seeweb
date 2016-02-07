from jinja2 import Markup
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.model_access import get_user

from seeweb.security import log_user_in, check_password


@view_config(route_name='user_login', renderer='templates/login.jinja2')
def view(request):
    if request.unauthenticated_userid is not None:
        request.session.flash("Already logged in, log out first", 'warning')
        return HTTPFound(location=request.route_url('home'))

    if "ok" in request.params:
        session = DBSession()

        uid = request.params["user_id"]
        user = get_user(session, uid)
        if user is None:
            msg = "No such user! <a href='%s'>Register?</a>" % request.route_url('user_register')
            request.session.flash(Markup(msg), 'warning')
            return HTTPFound(location=request.current_route_url())

        pwd = request.params["password"]
        # check password
        if check_password(session, user, pwd):
            return log_user_in(request, uid)
        else:
            request.session.flash("Invalid password", 'warning')
            return HTTPFound(location=request.current_route_url())
    else:
        return {}
