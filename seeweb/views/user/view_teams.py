from jinja2 import Markup
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.auth import Role
from seeweb.model_access import get_team, team_access_role
from seeweb.model_edit import add_team_auth, create_team

from .commons import view_init


def register_new_team(request, session, user):
    """Create a new team.

    Args:
        request: (Request)
        session: (DBSession)
        user: (User) user creating the team

    Returns:
        (None|tid): None if something failed, tid otherwise
    """
    tid = request.params.get('team_id', "")
    if len(tid) == 0:
        request.session.flash("Enter a team id first", 'warning')
        return None

    tid = tid.lower().strip()
    if " " in tid:
        msg = "Team id ('%s') cannot have space" % tid
        request.session.flash(msg, 'warning')
        return None

    team = get_team(session, tid)
    if team is not None:
        team_url = request.route_url('team_view_home', tid=tid)
        msg = "Team <a href='%s'>'%s'</a> already exists" % (team_url,
                                                             tid)
        request.session.flash(Markup(msg), 'warning')
        return None

    # create new team
    team = create_team(session, tid)
    add_team_auth(session, team, user, Role.edit)
    request.session.flash("New team %s created" % tid, 'success')
    return tid


@view_config(route_name='user_view_teams',
             renderer='templates/user/view_teams.jinja2')
def view(request):
    session = DBSession()
    user, view_params = view_init(request, session, 'teams')

    if 'new_team' in request.params and user.id == request.unauthenticated_userid:
        tid = register_new_team(request, session, user)
        if tid is not None:
            loc = request.route_url("team_view_home", tid=tid)
            return HTTPFound(location=loc)

    teams = []
    for actor in user.teams:
        team = get_team(session, actor.team)
        role = team_access_role(session, team, request.unauthenticated_userid)
        if role != Role.denied:
            teams.append((role, team))

    view_params['teams'] = teams

    return view_params
