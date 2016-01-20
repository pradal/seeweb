from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.access import project_access_role
from seeweb.models.auth import Role
from seeweb.models.project import Project


@view_config(route_name='project_list',
             renderer='templates/project/listing.jinja2')
def view(request):
    session = DBSession()
    current_uid = request.unauthenticated_userid

    query = session.query(Project)
    if 'query' in request.params and "all" not in request.params:
        search_pattern = "%s%%" % request.params['query']
        query = query.filter(Project.id.like(search_pattern))
    else:
        search_pattern = ""

    query = query.order_by(Project.id)
    projects = []
    for project in query.all():
        role = project_access_role(session, project, current_uid)
        if role != Role.denied:
            projects.append((role, project))

    return {'projects': projects,
            'search_pattern': search_pattern}

