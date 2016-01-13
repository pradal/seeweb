from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from seeweb.models.auth import Role
from seeweb.views.user.tools import get_user
from seeweb.views.tools import get_current_uid

from .tools import get_team


@view_config(route_name='team_home', renderer='templates/team/home.jinja2')
def index(request):
    tid = request.matchdict['tid']
    team = get_team(request, tid)
    current_uid = get_current_uid(request)

    allow_view = team.public
    if not allow_view:
        for actor in team.auth:
            if actor.user == current_uid:
                allow_view = (actor.role != Role.denied)

    if not allow_view:  # use auth list
        request.session.flash("Access to %s not granted for you" % tid,
                              'warning')
        return HTTPFound(location=request.route_url('home'))

    members = []
    allow_edit = False

    for actor in team.auth:
        if actor.user == current_uid:
            allow_edit = (actor.role == Role.edit)
            members.append((actor.role, actor.user))
        else:
            user = get_user(request, actor.user)
            if user.public_profile:
                members.append((actor.role, actor.user))

    return {"team": team, "allow_edit": allow_edit, "members": members}
