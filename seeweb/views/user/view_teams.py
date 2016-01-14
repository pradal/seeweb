from jinja2 import Markup
from pyramid.view import view_config

from seeweb.models.auth import Role
from seeweb.views.team.tools import create_team, get_team

from .tools import view_init


@view_config(route_name='user_view_teams', renderer='templates/user/view_teams.jinja2')
def index(request):
    user, current_uid, allow_edit = view_init(request)

    if 'new_team' in request.params:
        tid = request.params.get('team_id', "")
        if len(tid) > 0:
            tid = tid.lower().strip()
            if " " in tid:
                request.session.flash("Team id ('%s') cannot have space" % tid, 'warning')
            else:
                team = get_team(request, tid)
                if team is not None:
                    if team.public:
                        team_url = request.route_url('team_view_home', tid=tid)
                        msg = "Team <a href='%s'>'%s'</a> already exists" % (team_url, tid)
                        request.session.flash(Markup(msg), 'warning')
                    else:
                        request.session.flash("Team '%s' already exists (private)" % tid, 'warning')
                else:
                    # create new team
                    team = create_team(tid)
                    team.add_auth(user, Role.edit)
                    request.session.flash("New team %s created" % tid, 'success')

    teams = []
    for team in user.teams:
        role = team.access_role(current_uid)
        if role != Role.denied:
            teams.append((role, team))

    return {"user": user,
            "tab": 'teams',
            "allow_edit": allow_edit,
            "teams": teams}
