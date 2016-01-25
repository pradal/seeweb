from jinja2 import Markup
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.auth import Role
from seeweb.models.access import get_team, team_access_role
from seeweb.models.edit import create_team

from .tools import view_init, tabs


def register_new_team(request, session, uid):
    tid = request.params.get('team_id', "")
    if len(tid) == 0:
        request.session.flash("Enter a team id first", 'warning')
    else:
        tid = tid.lower().strip()
        if " " in tid:
            msg = "Team id ('%s') cannot have space" % tid
            request.session.flash(msg, 'warning')
        else:
            team = get_team(session, tid)
            if team is not None:
                team_url = request.route_url('team_view_home', tid=tid)
                msg = "Team <a href='%s'>'%s'</a> already exists" % (team_url,
                                                                     tid)
                request.session.flash(Markup(msg), 'warning')
            else:
                # create new team
                team = create_team(session, tid)
                team.add_auth(session, uid, Role.edit)
                request.session.flash("New team %s created" % tid, 'success')


@view_config(route_name='user_view_teams',
             renderer='templates/user/view_teams.jinja2')
def index(request):
    session = DBSession()
    user, view_params = view_init(request, session, 'teams')

    current_uid = view_params["current_uid"]

    if 'new_team' in request.params:
        register_new_team(request, session, current_uid)

    teams = []
    for actor in user.teams:
        team = get_team(session, actor.team)
        role = team_access_role(session, team, current_uid)
        if role != Role.denied:
            teams.append((role, team))

    view_params['teams'] = teams

    return view_params
