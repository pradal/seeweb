from pyramid.httpexceptions import HTTPFound

from seeweb.model_access import get_user


tabs = [('Home', 'home'),
        ('Projects', 'projects'),
        ('Teams', 'teams')]


def view_init(request, session, tab):
    """Common init for all 'view'.

    Args:
        request: (Request)
        session: (DBSession)
        tab: (str) current tab in view

    Returns:
        (User, dict of (str: any)): user, view_params
    """
    uid = request.matchdict['uid']
    user = get_user(session, uid)
    if user is None:
        request.session.flash("User %s does not exists" % uid, 'warning')
        raise HTTPFound(location=request.route_url('home'))

    current_uid = request.unauthenticated_userid

    view_params = {"user": user,
                   "tabs": tabs,
                   "tab": tab,
                   "allow_edit": (uid == current_uid),
                   "sections": []}

    return user, view_params


def edit_init(request, session, tab):
    """Common init for all 'edit' views.

    Args:
        request: (request)
        session: (DBSession)
        tab: (str) currently edited tab

    Returns:
        (User, dict of (str: any)): user, view_params
    """
    user, view_params = view_init(request, session, tab)

    if not view_params["allow_edit"]:
        msg = "Access to %s edition not granted for you" % user.id
        request.session.flash(msg, 'warning')
        raise HTTPFound(location=request.route_url('home'))

    if 'back' in request.params:
        request.session.flash("Edition stopped", 'success')
        raise HTTPFound(location=request.route_url('user_view_%s' % tab,
                                                   uid=user.id))

    return user, view_params


def edit_common(request, session, user):
    """Common edition operations.

    Args:
        request: (Request)
        session: (DBSession)
        user: (User) user to be edited

    Returns:
        (Bool): whether user has changed and the view needs to be reloaded
    """
    del session
    need_reload = False
    if 'name' in request.params:
        name = request.params['name']
        if user.name != name:
            user.name = name
            need_reload = True

    return need_reload
