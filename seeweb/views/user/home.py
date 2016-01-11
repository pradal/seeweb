from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.user import User
from seeweb.views.tools import get_current_uid


@view_config(route_name='user_home', renderer='templates/user/home.jinja2')
def index(request):
    uid = request.matchdict['uid']
    session = DBSession()

    users = session.query(User).filter(User.username == uid).all()
    if len(users) == 0:
        request.session.flash("User %s does not exists" % uid, 'warning')
        return HTTPFound(location=request.route_url('home'))

    current_uid = get_current_uid(request)
    if uid != current_uid:
        request.session.flash("Access to %s not granted for you" % uid,
                              'warning')
        return HTTPFound(location=request.route_url('home'))

    user, = users

    return {"user": user}
