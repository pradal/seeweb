from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from seeweb.models.auth import Role
from seeweb.views.tools import get_current_uid

from .tools import get_team


@view_config(route_name='team_edit',
             renderer='templates/team/edit.jinja2')
def view(request):
    tid = request.matchdict['tid']
    current_uid = get_current_uid(request)

    team = get_team(request, tid)

    allow_edit = False
    for actor in team.auth:
        if actor.user == current_uid:
            allow_edit = (actor.role == Role.edit)

    if not allow_edit:
        request.session.flash("Access to %s edition not granted for you" % tid,
                              'warning')
        return HTTPFound(location=request.route_url('home'))

    if 'cancel' in request.params:
        request.session.flash("Edition cancelled", 'success')
        return HTTPFound(location=request.route_url('team_home', tid=tid))

    if 'default' in request.params:
        # reload default values for this user
        # actually already done
        pass
    elif 'update' in request.params:
        # edit team visibility
        public = 'visibility' in request.params
        team.public = public
    else:
        pass

    return {'team': team}
