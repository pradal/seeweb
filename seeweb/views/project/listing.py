from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.auth import Role
from seeweb.models.project import Project


@view_config(route_name='project_list',
             renderer='templates/project/listing.jinja2')
def view(request):
    session = DBSession()
    query = session.query(Project)

    search_pattern = request.params.get("main_search", "")
    if search_pattern != "":
        query = query.filter(Project.id.like("%s%%" % search_pattern))

    query = query.order_by(Project.id)
    projects = []
    for project in query.all():
        role = project.access_role(session, request.unauthenticated_userid)
        if role != Role.denied:
            projects.append((Role.to_str(role), project))

    return {'projects': projects,
            'search_pattern': search_pattern}
