from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.project import Project


@view_config(route_name='admin_projects',
             renderer='templates/admin/projects.jinja2',
             permission='admin')
def view(request):
    session = DBSession()
    query = session.query(Project)

    search_pattern = request.params.get("main_search", "")
    if search_pattern != "":
        query = query.filter(Project.id.like("%s%%" % search_pattern))

    if 'delete' in request.params:
        print "DELETE", request.params, "\n" * 10

    return {'projects': query.all(),
            'search_pattern': search_pattern}
