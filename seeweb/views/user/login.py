from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.user import User
from seeweb.views.tools import set_current_uid


@view_config(route_name='user_login', renderer='templates/user/login.jinja2')
def index(request):
    if "ok" in request.params:
        session = DBSession()
        query = session.query(User)

        username = request.params["username"]
        query = query.filter(User.username.like(username))
        if len(query.all()) == 0:
            request.session.flash("No such user", 'warning')
            return HTTPFound(location=request.route_url('user_login'))

        set_current_uid(request, username)
        return HTTPFound(location=request.route_url('user_home', uid=username))
    elif 'cancel' in request.params:
        return HTTPFound(location=request.route_url('home'))
    else:
        return {}
