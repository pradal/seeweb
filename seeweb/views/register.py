from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.user import User

from .tools import set_current_uid


@view_config(route_name='user_register', renderer='templates/register.jinja2')
def index(request):
    if "ok" in request.params:
        session = DBSession()
        query = session.query(User)

        uid = request.params["user_id"]
        if len(uid) == 0:  # test user_id validity
            request.session.flash("No user id given", 'warning')
            return HTTPFound(location=request.route_url('user_register'))

        query = query.filter(User.id.like(uid))
        if len(query.all()) != 0:
            request.session.flash("User %s already exists" % uid, 'warning')
            return HTTPFound(location=request.route_url('user_register'))
        else:
            user = User(id=uid)
            session.add(user)

            set_current_uid(request, uid)
            return HTTPFound(location=request.route_url('user_view_home', uid=uid))
    else:
        return {}
