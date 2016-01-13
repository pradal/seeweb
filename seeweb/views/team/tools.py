from pyramid.httpexceptions import HTTPFound

from seeweb.models import DBSession
from seeweb.models.team import Team


def get_team(request, tid):
    session = DBSession()
    teams = session.query(Team).filter(Team.name == tid).all()
    if len(teams) == 0:
        request.session.flash("Team %s does not exists" % tid, 'warning')
        return HTTPFound(location=request.route_url('home'))

    team, = teams

    return team
