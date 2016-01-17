from pyramid.httpexceptions import HTTPFound

from seeweb.models.auth import Role
from seeweb.models.access import get_team, team_access_role
from seeweb.views.tools import get_current_uid

tabs = [('Home', 'home'),
        ('Projects', 'projects'),
        ('Members', 'members')]


def view_init(request):
    """Common init for all 'view' parts
    """
    tid = request.matchdict['tid']
    team = get_team(tid)
    if team is None:
        request.session.flash("Team %s does not exists" % tid, 'warning')
        return None, HTTPFound(location=request.route_url('home')), None

    current_uid = get_current_uid(request)

    # allow edition
    allow_edit = (team_access_role(team, current_uid) == Role.edit)

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
    pass
