from pyramid.httpexceptions import HTTPFound

from seeweb.models.access import get_project
from seeweb.models.auth import Role
from seeweb.views.tools import get_current_uid

tabs = [('Home', 'home'),
        ('Documentation', 'doc'),
        ('Source', 'source'),
        ('Contributors', 'contributors'),
        ('Comments', 'comments')]


def view_init(request):
    """Common init for all 'view' parts
    """
    pid = request.matchdict['pid']

    project = get_project(pid)
    if project is None:
        request.session.flash("Project %s does not exists" % pid, 'warning')
        return None, HTTPFound(location=request.route_url('home'))

    current_uid = get_current_uid(request)
    role = project.access_role(current_uid)
    if role == Role.denied:
        request.session.flash("Access to %s not granted for you" % pid,
                              'warning')
        return None, HTTPFound(location=request.route_url('home'))

    allow_edit = (role == Role.edit)

    return project, allow_edit


def edit_init(request):
    """Common init for all 'edit' views.
    """
    project, allow_edit = view_init(request)

    if not allow_edit:
        request.session.flash("Access to %s edition not granted for you" % project.id,
                              'warning')
        return None, HTTPFound(location=request.route_url('home'))

    return project, allow_edit


def edit_common(request, project):
    """Common edition operations
    """
    # edit team visibility
    public = 'visibility' in request.params
    project.public = public
