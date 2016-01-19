from pyramid.httpexceptions import HTTPFound

from seeweb.models.access import get_user
from seeweb.views.tools import get_current_uid


tabs = [('Home', 'home'),
        ('Projects', 'projects'),
        ('Teams', 'teams')]


def view_init(request, session):
    """Common init for all 'view'.
    """
    uid = request.matchdict['uid']
    user = get_user(session, uid)
    if user is None:
        request.session.flash("User %s does not exists" % uid, 'warning')
        raise HTTPFound(location=request.route_url('home'))

    current_uid = get_current_uid(request)
    allow_edit = (uid == current_uid)

    return user, current_uid, allow_edit


def edit_init(request, session):
    """Common init for all 'edit' views.
    """
    user, current_uid, allow_edit = view_init(request, session)

    if not allow_edit:
        msg = "Access to %s edition not granted for you" % user.id
        request.session.flash(msg, 'warning')
        raise HTTPFound(location=request.route_url('home'))

    return user, current_uid


def edit_common(request, session, user):
    """Common edition operations
    """
    del session
    need_reload = False
    if 'name' in request.params:
        name = request.params['name']
        if user.name != name:
            user.name = name
            need_reload = True

    return need_reload
