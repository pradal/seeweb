from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.team import Team


@view_config(route_name='admin_teams',
             renderer='templates/admin/teams.jinja2',
             permission='admin')
def view(request):
    session = DBSession()
    query = session.query(Team)
    if 'query' in request.params and "all" not in request.params:
        search_pattern = "%s%%" % request.params['query']
        query = query.filter(Team.id.like(search_pattern))
    else:
        search_pattern = ""

    return {'teams': query.all(),
            'search_pattern': search_pattern}
