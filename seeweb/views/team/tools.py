from pyramid.httpexceptions import HTTPFound

from seeweb.models import DBSession
from seeweb.models.auth import Role
from seeweb.models.edit import create_team
from seeweb.models.team import Team
from seeweb.views.tools import get_current_uid

tabs = [('Home', 'home'),
        ('Projects', 'projects'),
        ('Members', 'members')]


def get_team(request, tid):
    session = DBSession()
    teams = session.query(Team).filter(Team.id == tid).all()
    if len(teams) == 0:
        return None

    team, = teams

    return team


def register_team(tid):
    """Create a new team.

    Does not test existence of team beforehand
    """
    session = DBSession()
    team = create_team(tid)
    session.add(team)

    return team


def view_init(request):
    """Common init for all 'view' parts
    """
    tid = request.matchdict['tid']
    team = get_team(request, tid)
    if team is None:
        request.session.flash("Team %s does not exists" % tid, 'warning')
        return None, HTTPFound(location=request.route_url('home')), None

    current_uid = get_current_uid(request)

    allow_view = team.public
    if not allow_view:
        for actor in team.auth:
            if actor.user == current_uid:
                allow_view = (actor.role != Role.denied)

    if not allow_view:  # use auth list
        request.session.flash("Access to %s not granted for you" % tid,
                              'warning')
        return None, HTTPFound(location=request.route_url('home')), None

    # allow edition
    allow_edit = False
    i, actor = team.get_actor(current_uid)
    if actor is not None:
        allow_edit = (actor.role == Role.edit)

    return team, current_uid, allow_edit


def edit_init(request):
    """Common init for all 'edit' views.
    """
    team, current_uid, allow_edit = view_init(request)

    if not allow_edit:
        request.session.flash("Access to %s edition not granted for you" % team.id,
                              'warning')
        return None, HTTPFound(location=request.route_url('home'))

    return team, current_uid


def edit_common(request, team):
    """Common edition operations
    """
    # edit team visibility
    public = 'visibility' in request.params
    team.public = public
