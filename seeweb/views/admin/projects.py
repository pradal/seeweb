from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.project import Project


@view_config(route_name='admin_projects',
             renderer='templates/admin/projects.jinja2')
def view(request):
    session = DBSession()
    query = session.query(Project)
    if 'query' in request.params:
        search_pattern = "%s%%" % request.params['query']
        query = query.filter(Project.name.like(search_pattern))
    else:
        search_pattern = ""

    projects = query.all()
    print "projects", projects
    for i, project in enumerate(projects):
        if i % 2 == 0:
            project.parity = "even"
        else:
            project.parity = "odd"

    return {'projects': projects, 'search_pattern': search_pattern}
