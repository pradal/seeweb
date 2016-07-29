from pyramid.httpexceptions import HTTPFound
import transaction

from seeweb.models.auth import Role
from seeweb.models.research_object import ResearchObject
from seeweb.models.ro_link import ROLink
from seeweb.models.user import User


tabs = [('Home', 'home'),
        ('Actors', 'actors'),
        ('Links', 'links')]


def fetch_ro(request, session):
    """Retrieve RO whose id is in URL.

    Args:
        request: (Request)
        session: (DBSession)

    Returns:
        (str, ResearchObject): uid, ro
    """
    uid = request.matchdict['uid']
    ro = ResearchObject.get(session, uid)
    if ro is None:
        request.session.flash("RO %s does not exists" % uid, 'warning')
        raise HTTPFound(location=request.route_url('home'))

    return uid, ro


def fetch_containers(session, ro):
    """Retrieve ids of all containers holding this RO

    Args:
        session (DBSession):
        ro (ResearchObject):

    Returns:
        (list of str)
    """
    query = session.query(ROLink.source)
    query = query.filter(ROLink.type == 'contains')
    query = query.filter(ROLink.target == ro.id)

    return [uid for uid, in query.all()]


def view_init_min(request, session):
    """Common init for all 'view' parts.

    Args:
        request: (Request)
        session: (DBSession)

    Returns:
        (ResearchObject, dict of (str: any)): ro, view_params
    """
    uid, ro = fetch_ro(request, session)

    current_uid = request.unauthenticated_userid

    role = ro.access_role(session, current_uid)
    if role == Role.denied:
        request.session.flash("Access to %s not granted for you" % uid,
                              'warning')
        raise HTTPFound(location=request.route_url('home'))

    # find containers
    uids = fetch_containers(session, ro)
    containers = [(uid, ResearchObject.get(session, uid).name) for uid in uids]

    # allow edition
    allow_edit = (current_uid is not None and role == Role.edit)

    view_params = {"ro": ro,
                   "containers": containers,
                   "allow_edit": allow_edit,
                   "minimized": True}

    return ro, view_params


def view_init(request, session, tab):
    """Extended init adding tabs.

    Args:
        request: (Request)
        session: (DBSession)
        tab: (str) current tab in view

    Returns:
        (ResearchObject, dict of (str: any)): ro, view_params
    """
    ro, view_params = view_init_min(request, session)

    view_params["tabs"] = tabs
    view_params["tab"] = tab
    view_params["sections"] = []

    return ro, view_params


def edit_init(request, session, tab):
    """Common init for all 'edit' views.

    Args:
        request: (Request)
        session: (DBSession)
        tab: (str) current tab in view

    Returns:
        (ResearchObject, dict of (str: any)): ro, view_params
    """
    ro, view_params = view_init(request, session, tab)

    warn_links = [link for link in ro.out_links if link.type == 'produce']
    error_links = [link for link in ro.in_links if link.type != 'contains']
    view_params["warn_links"] = warn_links
    view_params["error_links"] = error_links

    if not view_params["allow_edit"]:
        msg = "Access to %s edition not granted for you" % ro.id
        request.session.flash(msg, 'warning')
        raise HTTPFound(location=request.route_url('home'))

    if 'back' in request.params:
        # request.session.flash("Edition stopped", 'success')
        loc = request.route_url('ro_view_%s' % tab, uid=ro.id)
        raise HTTPFound(location=loc)

    if 'update' in request.params:
        # edit project visibility
        public = 'visibility' in request.params
        ro.public = public

    if 'confirm_transfer' in request.params:
        if request.unauthenticated_userid != ro.owner:
            request.session.flash("Action non authorized for you", 'warning')
            raise HTTPFound(location=request.route_url('home'))

        user = User.get(session, request.params["new_owner"])
        if user is None:
            msg = "User '%s' is unknown" % request.params["new_owner"]
            request.session.flash(msg, 'warning')
            raise HTTPFound(location=request.current_route_url())

        ro.change_owner(session, user)
        loc = request.route_url("ro_view_home", uid=ro.id)
        transaction.commit()
        raise HTTPFound(location=loc)

    delete_recursive = "confirm_delete_recursive" in request.params
    if "confirm_delete" in request.params or delete_recursive:
        if ResearchObject.remove(session, ro, delete_recursive):
            transaction.commit()
            request.session.flash("RO '%s' deleted" % ro.id, 'success')
        else:
            request.session.flash("Failed to delete '%s'" % ro.id, 'warning')
        raise HTTPFound(location=request.route_url('home'))

    return ro, view_params
