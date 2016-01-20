from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.access import get_user

from .tools import log_user


@view_config(route_name='user_login', renderer='templates/login.jinja2')
def index(request):
    if "ok" in request.params:
        session = DBSession()

        uid = request.params["user_id"]
        user = get_user(session, uid)
        if user is None:
            request.session.flash("No such user", 'warning')
            return HTTPFound(location=request.route_url('user_login'))

        return log_user(request, uid)
    else:
        return {}
