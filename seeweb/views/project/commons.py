from pyramid.httpexceptions import HTTPFound

from seeweb.model_access import get_project, get_user, project_access_role
from seeweb.models.auth import Role

tabs = [('Home', 'home'),
        ('Documentation', 'doc'),
        ('Source', 'source'),
        ('Contributors', 'contributors'),
        ('Comments', 'comments')]


def view_init(request, session, tab):
    """Common init for all 'view'.

    Args:
        request: (Request)
        session: (DBSession)
        tab: (str) current tab in view

    Returns:
        (User, dict of (str: any)): user, view_params
    """
    pid = request.matchdict['pid']

    project = get_project(session, pid)
    if project is None:
        request.session.flash("Project %s does not exists" % pid, 'warning')
        raise HTTPFound(location=request.route_url('home'))

    current_uid = request.unauthenticated_userid
    role = project_access_role(session, project, current_uid)
    if role == Role.denied:
        request.session.flash("Access to %s not granted for you" % pid,
                              'warning')
        raise HTTPFound(location=request.route_url('home'))

    # potential install
    if current_uid is None:  # TODO can do better
        install_action = None
    else:
        user = get_user(session, current_uid)
        if project in user.installed:
            install_action = "uninstall"
        else:
            install_action = "install"

    view_params = {"current_uid": current_uid,
                   "project": project,
                   "tabs": tabs,
                   "tab": tab,
                   "allow_edit": (role == Role.edit),
                   "install_action": install_action,
                   "sections": [],
                   "ratings": project.format_ratings()}

    return project, view_params


def edit_init(request, session, tab):
    """Common init for all 'edit' views.

    Args:
        request: (request)
        session: (DBSession)
        tab: (str) currently edited tab

    Returns:
        (User, dict of (str: any)): user, view_params
    """
    project, view_params = view_init(request, session, tab)

    if not view_params["allow_edit"]:
        msg = "Access to %s edition not granted for you" % project.id
        request.session.flash(msg, 'warning')
        raise HTTPFound(location=request.route_url('home'))

    if 'back' in request.params:
        request.session.flash("Edition stopped", 'success')
        loc = request.route_url('project_view_%s' % tab, pid=project.id)
        raise HTTPFound(location=loc)

    if 'delete' in request.params:
        request.session.flash("Edition stopped", 'success')
        loc = request.route_url('home')
        raise HTTPFound(location=loc)

    return project, view_params


def edit_common(request, session, project):
    """Common edition operations.

    Args:
        request: (Request)
        session: (DBSession)
        project: (Project) project to be edited

    Returns:
        (Bool): whether project has changed and the view needs to be reloaded
    """
    del session

    # edit project visibility
    public = 'visibility' in request.params
    project.public = public

    return False
