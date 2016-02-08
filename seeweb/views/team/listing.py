from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.team import Team


@view_config(route_name='team_list',
             renderer='templates/team/listing.jinja2')
def view(request):
    session = DBSession()
    query = session.query(Team)

    search_pattern = request.params.get("main_search", "")
    if search_pattern != "":
        query = query.filter(Team.id.like("%s%%" % search_pattern))

    query = query.order_by(Team.id)
    teams = query.all()

    return {'teams': teams,
            'search_pattern': search_pattern}
