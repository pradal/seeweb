from pyramid.httpexceptions import HTTPFound

from seeweb.models.auth import Role
from seeweb.models.access import get_team, team_access_role

tabs = [('Home', 'home'),
        ('Projects', 'projects'),
        ('Members', 'members')]


def view_init(request, session):
    """Common init for all 'view' parts
    """
    tid = request.matchdict['tid']
    team = get_team(session, tid)
    if team is None:
        request.session.flash("Team %s does not exists" % tid, 'warning')
        raise HTTPFound(location=request.route_url('home'))

    current_uid = request.unauthenticated_userid

    # allow edition
    allow_edit = (current_uid is not None and
                  team_access_role(session, team, current_uid) == Role.edit)

    return team, current_uid, allow_edit


def edit_init(request, session):
    """Common init for all 'edit' views.
    """
    team, current_uid, allow_edit = view_init(request, session)

    if not allow_edit:
        msg = "Access to %s edition not granted for you" % team.id
        request.session.flash(msg, 'warning')
        raise HTTPFound(location=request.route_url('home'))

    return team, current_uid


def edit_common(request, session, team):
    """Common edition operations
    """
    del request
    del session
    del team
    return False
