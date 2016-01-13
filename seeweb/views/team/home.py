from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from seeweb.models.auth import access_role, Role
from seeweb.views.tools import get_current_uid

from .tools import get_team


@view_config(route_name='team_home', renderer='templates/team/home.jinja2')
def index(request):
    tid = request.matchdict['tid']
    team = get_team(request, tid)
    current_uid = get_current_uid(request)

    if not team.public:  # use auth list
        request.session.flash("Access to %s not granted for you" % tid,
                              'warning')
        return HTTPFound(location=request.route_url('home'))

    return {"team": team}
