from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.user import User

from .tools import set_current_uid


@view_config(route_name='user_login', renderer='templates/login.jinja2')
def index(request):
    if "ok" in request.params:
        session = DBSession()
        query = session.query(User)

        uid = request.params["user_id"]
        query = query.filter(User.id.like(uid))
        if len(query.all()) == 0:
            request.session.flash("No such user", 'warning')
            return HTTPFound(location=request.route_url('user_login'))

        set_current_uid(request, uid)
        return HTTPFound(location=request.route_url('user_home', uid=uid))
    else:
        return {}
