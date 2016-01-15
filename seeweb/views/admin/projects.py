from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.project import Project


@view_config(route_name='admin_projects',
             renderer='templates/admin/projects.jinja2')
def view(request):
    session = DBSession()
    query = session.query(Project)
    if 'query' in request.params and "all" not in request.params:
        search_pattern = "%s%%" % request.params['query']
        query = query.filter(Project.id.like(search_pattern))
    else:
        search_pattern = ""

    return {'projects': query.all(), 'search_pattern': search_pattern}
