from pyramid.httpexceptions import HTTPFound

from seeweb.models import DBSession
from seeweb.models.auth import Role
from seeweb.models.edit import create_project
from seeweb.models.project import Project
from seeweb.views.tools import get_current_uid


def get_project(request, pid):
    session = DBSession()

    projects = session.query(Project).filter(Project.id == pid).all()
    if len(projects) == 0:
        return None

    project, = projects

    return project


def register_project(owner, pid):
    """Create a new project and register it.
    """
    session = DBSession()
    project = create_project(owner, pid, public=False)
    session.add(project)

    return project


def view_init(request):
    """Common init for all 'view' parts
    """
    pid = request.matchdict['pid']

    project = get_project(request, pid)
    if project is None:
        request.session.flash("Project %s does not exists" % pid, 'warning')
        return None, HTTPFound(location=request.route_url('home'))

    current_uid = get_current_uid(request)
    role = project.access_role(current_uid)
    if role == Role.denied:
        request.session.flash("Access to %s not granted for you" % pid,
                              'warning')
        return None, HTTPFound(location=request.route_url('home'))

    allow_edit = role == Role.edit

    return project, allow_edit