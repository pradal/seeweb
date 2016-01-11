from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.user import User
from seeweb.views.tools import set_current_uid


@view_config(route_name='user_register', renderer='templates/user/register.jinja2')
def index(request):
    if "ok" in request.params:
        session = DBSession()
        query = session.query(User)

        username = request.params["username"]
        if len(username) == 0:  # test username validity
            request.session.flash("No username", 'warning')
            return HTTPFound(location=request.route_url('user_register'))

        query = query.filter(User.username.like(username))
        if len(query.all()) != 0:
            request.session.flash("User %s already exists" % username, 'warning')
            return HTTPFound(location=request.route_url('user_register'))
        else:
            name = request.params["name"]
            if len(name) == 0:
                request.session.flash("No display name", 'warning')
                return HTTPFound(location=request.route_url('user_register'))

            email = request.params["email"]
            if len(email) == 0:  # test email validity
                request.session.flash("No email", 'warning')
                return HTTPFound(location=request.route_url('user_register'))

            user = User(username=username, name=name, email=email)
            session.add(user)

            set_current_uid(request, username)
            return HTTPFound(location=request.route_url('user_home', uid=username))
    elif 'cancel' in request.params:
        return HTTPFound(location=request.route_url('home'))
    else:
        return {}
