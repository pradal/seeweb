from pyramid.httpexceptions import HTTPFound

from seeweb.models import DBSession
from seeweb.models.user import User


def get_user(request, uid):
    session = DBSession()
    users = session.query(User).filter(User.id == uid).all()
    if len(users) == 0:
        request.session.flash("User %s does not exists" % uid, 'warning')
        return HTTPFound(location=request.route_url('home'))

    user, = users

    return user
