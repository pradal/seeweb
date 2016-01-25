from pyramid.httpexceptions import HTTPFound

from seeweb.models.access import get_user


tabs = [('Home', 'home'),
        ('Projects', 'projects'),
        ('Teams', 'teams'),
        ("Playground", "playground")]


def view_init(request, session, tab):
    """Common init for all 'view'.
    """
    uid = request.matchdict['uid']
    user = get_user(session, uid)
    if user is None:
        request.session.flash("User %s does not exists" % uid, 'warning')
        raise HTTPFound(location=request.route_url('home'))

    current_uid = request.unauthenticated_userid

    if uid == current_uid:
        itabs = len(tabs)
    else:
        itabs = len(tabs) - 1

    view_params = {"current_uid": current_uid,
                   "user": user,
                   "tabs": tabs[:itabs],
                   "tab": tab,
                   "allow_edit": (uid == current_uid),
                   "sections": []}

    return user, view_params


def edit_init(request, session, tab):
    """Common init for all 'edit' views.
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
