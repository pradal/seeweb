from pyramid.httpexceptions import HTTPFound

from seeweb.models import DBSession
from seeweb.views.tools import get_current_uid
from seeweb.models.user import User


tabs = [('Home', 'home'),
        ('Projects', 'projects'),
        ('Teams', 'teams')]


def get_user(uid):
    session = DBSession()
    users = session.query(User).filter(User.id == uid).all()
    if len(users) == 0:
        return None

    user, = users

    return user


def view_init(request):
    """Common init for all 'view'.
    """
    uid = request.matchdict['uid']
    user = get_user(uid)
    if user is None:
        request.session.flash("User %s does not exists" % uid, 'warning')
        return HTTPFound(location=request.route_url('home'))

    current_uid = get_current_uid(request)
    allow_edit = (uid == current_uid)

    return user, current_uid, allow_edit


def edit_init(request):
    """Common init for all 'edit' views.
    """
    uid = request.matchdict['uid']
    current_uid = get_current_uid(request)

    if uid != current_uid:
        request.session.flash("Access to %s edition not granted for you" % uid,
                              'warning')
        return None, HTTPFound(location=request.route_url('home'))

    user = get_user(uid)
    if user is None:
        request.session.flash("User %s does not exists" % uid, 'warning')
        return None, HTTPFound(location=request.route_url('home'))

    return user, current_uid


def edit_common(request, user):
    """Common edition operations
    """
    pass
