from pyramid.httpexceptions import HTTPFound

from seeweb.models import DBSession
from seeweb.models.auth import Role
from seeweb.models.team import Team
from seeweb.views.tools import get_current_uid


def get_team(request, tid):
    session = DBSession()
    teams = session.query(Team).filter(Team.id == tid).all()
    if len(teams) == 0:
        request.session.flash("Team %s does not exists" % tid, 'warning')
        return HTTPFound(location=request.route_url('home'))

    team, = teams

    return team


def view_init(request):
    """Common init for all 'view' parts
    """
    tid = request.matchdict['tid']
    team = get_team(request, tid)
    current_uid = get_current_uid(request)

    tab = 0

    allow_view = team.public
    if not allow_view:
        for actor in team.auth:
            if actor.user == current_uid:
                allow_view = (actor.role != Role.denied)

    if not allow_view:  # use auth list
        request.session.flash("Access to %s not granted for you" % tid,
                              'warning')
        return HTTPFound(location=request.route_url('home'))

    allow_edit = False
    i, actor = team.get_actor(current_uid)
    if actor is not None:
        allow_edit = (actor.role == Role.edit)

    return tid, team, current_uid, allow_edit
