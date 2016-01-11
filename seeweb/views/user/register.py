from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.user import User


@view_config(route_name='user_register', renderer='templates/user/register.jinja2')
def index(request):
    if "ok" in request.params:
        session = DBSession()
        query = session.query(User)

        email = request.params["email"]
        if len(email) == 0:  # test email validity
            request.session.flash("No email", 'warning')
            return HTTPFound(location=request.route_url('user_register'))

        query = query.filter(User.email.like(email))
        if len(query.all()) != 0:
            request.session.flash("User %s already exists" % email, 'warning')
            return HTTPFound(location=request.route_url('user_register'))
        else:
            display_name = request.params["display_name"]
            if len(display_name) == 0:
                request.session.flash("No display name", 'warning')
                return HTTPFound(location=request.route_url('user_register'))

            user = User(email=email, display_name=display_name)
            session.add(user)

            request.session["userid"] = email
            return HTTPFound(location=request.route_url('user_home'))
    elif 'cancel' in request.params:
        return HTTPFound(location=request.route_url('home'))
    else:
        return {}
