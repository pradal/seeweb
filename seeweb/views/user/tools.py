from pyramid.httpexceptions import HTTPFound

from seeweb.models import DBSession
from seeweb.views.tools import get_current_uid
from seeweb.models.user import User


def get_user(request, uid):
    session = DBSession()
    users = session.query(User).filter(User.id == uid).all()
    if len(users) == 0:
        request.session.flash("User %s does not exists" % uid, 'warning')
        return HTTPFound(location=request.route_url('home'))

    user, = users

    return user


def view_init(request):
    """Common init for all 'view'.
    """
    uid = request.matchdict['uid']
    user = get_user(request, uid)
    current_uid = get_current_uid(request)
    allow_edit = (uid == current_uid)

    return user, current_uid, allow_edit
