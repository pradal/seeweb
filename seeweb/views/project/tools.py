from pyramid.httpexceptions import HTTPFound

from seeweb.models.access import get_project, project_access_role
from seeweb.models.auth import Role
from seeweb.views.tools import get_current_uid

tabs = [('Home', 'home'),
        ('Documentation', 'doc'),
        ('Source', 'source'),
        ('Contributors', 'contributors'),
        ('Comments', 'comments')]


def view_init(request, session):
    """Common init for all 'view' parts
    """
    pid = request.matchdict['pid']

    project = get_project(session, pid)
    if project is None:
        request.session.flash("Project %s does not exists" % pid, 'warning')
        raise HTTPFound(location=request.route_url('home'))

    current_uid = get_current_uid(request)
    role = project_access_role(session, project, current_uid)
    if role == Role.denied:
        request.session.flash("Access to %s not granted for you" % pid,
                              'warning')
        raise HTTPFound(location=request.route_url('home'))

    allow_edit = (role == Role.edit)

    return project, allow_edit


def edit_init(request, session):
    """Common init for all 'edit' views.
    """
    project, allow_edit = view_init(request, session)

    if not allow_edit:
        msg = "Access to %s edition not granted for you" % project.id
        request.session.flash(msg, 'warning')
        raise HTTPFound(location=request.route_url('home'))

    return project, allow_edit


def edit_common(request, session, project):
    """Common edition operations
    """
    del session

    # edit team visibility
    public = 'visibility' in request.params
    project.public = public
