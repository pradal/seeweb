from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.team import Team


@view_config(route_name='admin_teams',
             renderer='templates/admin/teams.jinja2',
             permission='admin')
def view(request):
    session = DBSession()
    query = session.query(Team)

    search_pattern = request.params.get("main_search", "")
    if search_pattern != "":
        query = query.filter(Team.id.like("%s%%" % search_pattern))

    return {'teams': query.all(),
            'search_pattern': search_pattern}
