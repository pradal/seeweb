from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.auth import Role
from seeweb.models.team import Team


@view_config(route_name='team_list',
             renderer='templates/team/listing.jinja2')
def view(request):
    session = DBSession()
    query = session.query(Team)
    if 'query' in request.params and "all" not in request.params:
        search_pattern = "%s%%" % request.params['query']
        query = query.filter(Team.id.like(search_pattern))
    else:
        search_pattern = ""

    query = query.order_by(Team.id)
    teams = [(Role.read, team) for team in query.all()]

    return {'teams': teams,
            'search_pattern': search_pattern}

