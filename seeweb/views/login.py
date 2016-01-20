from jinja2 import Markup
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.access import get_user

from .tools import log_user, check_password


@view_config(route_name='user_login', renderer='templates/login.jinja2')
def index(request):
    if "ok" in request.params:
        session = DBSession()

        uid = request.params["user_id"]
        user = get_user(session, uid)
        if user is None:
            msg = "No such user! <a href='%s'>Register?</a>" % request.route_url('user_register')
            request.session.flash(Markup(msg), 'warning')
            return HTTPFound(location=request.route_url('user_login'))

        pwd = request.params["password"]
        # check password
        if check_password(session, user, pwd):
            return log_user(request, uid)
        else:
            request.session.flash("Invalid password", 'warning')
            return HTTPFound(location=request.route_url('user_login'))
    else:
        return {}
