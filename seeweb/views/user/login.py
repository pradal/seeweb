from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.user import User


@view_config(route_name='user_login', renderer='templates/user/login.jinja2')
def index(request):
    if "ok" in request.params:
        session = DBSession()
        query = session.query(User)

        email = request.params["email"]
        query = query.filter(User.email.like(email))
        if len(query.all()) == 0:
            request.session.flash("No such user", 'warning')
            return HTTPFound(location=request.route_url('user_login'))

        request.session["userid"] = email
        return HTTPFound(location=request.route_url('user_home'))
    elif 'cancel' in request.params:
        return HTTPFound(location=request.route_url('home'))
    else:
        return {}
