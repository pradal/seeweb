from pyramid.httpexceptions import HTTPFound

from seeweb.models import DBSession
from seeweb.models.auth import Role
from seeweb.models.comment import Comment
from seeweb.models.edit import create_project
from seeweb.models.project import Project
from seeweb.views.tools import get_current_uid

tabs = [('Home', 'home'),
        ('Documentation', 'doc'),
        ('Source', 'source'),
        ('Contributors', 'contributors'),
        ('Comments', 'comments')]


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


def fetch_comments(pid, limit=None):
    """Fectch all comments associated to a project.
    """
    session = DBSession()

    query = session.query(Comment).filter(Comment.project == pid).order_by(Comment.rating.desc())
    if limit is not None:
        query = query.limit(limit)

    comments = query.all()

    return comments


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
