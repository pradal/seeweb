from seeweb.models import DBSession
from seeweb.models.edit import create_project
from seeweb.models.project import Project


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
