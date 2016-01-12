from pyramid.httpexceptions import HTTPFound

from seeweb.models import DBSession
from seeweb.models.project import Project


def get_project(request, uid, pid):
    session = DBSession()

    projects = session.query(Project).filter(Project.name == pid).all()
    if len(projects) == 0:
        request.session.flash("Project %s does not exists" % pid, 'warning')
        return HTTPFound(location=request.route_url('home'))

    project, = projects
    if project.owner != uid:
        request.session.flash("Project %s does not exists" % pid, 'warning')
        return HTTPFound(location=request.route_url('home'))

    return project
