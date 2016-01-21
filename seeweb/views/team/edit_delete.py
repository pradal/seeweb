from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.access import get_team, team_access_role
from seeweb.models.auth import Role
from seeweb.models.edit import remove_team


@view_config(route_name='team_edit_delete',
             renderer='templates/team/edit_delete.jinja2')
def view(request):
    session = DBSession()
    tid = request.matchdict['tid']

    team = get_team(session, tid)
    if team is None:
        request.session.flash("Team %s does not exists" % tid, 'warning')
        raise HTTPFound(location=request.route_url('home'))

    current_uid = request.unauthenticated_userid
    role = team_access_role(session, team, current_uid)
    if role != Role.edit:
        request.session.flash("Delete %s not granted for you" % tid,
                              'warning')
        raise HTTPFound(location=request.route_url('home'))

    if 'cancel' in request.params:
        loc = request.route_url('team_view_home', tid=tid)
        raise HTTPFound(location=loc)

    if 'delete' in request.params:
        if remove_team(session, team):
            request.session.flash("Team %s has been deleted" % tid, 'success')
            loc = request.route_url('user_view_teams', uid=current_uid)
            return HTTPFound(location=loc)
        else:
            request.session.flash("Problem with deletion of " % tid, 'warning')
            loc = request.route_url('user_view_teams', uid=current_uid)
            return HTTPFound(location=loc)

    return {"team": team}
