from pyramid.httpexceptions import HTTPFound

from seeweb.models.auth import Role
from seeweb.models.team import Team
from seeweb.model_access import team_access_role
from seeweb.model_edit import remove_team
import transaction


tabs = [('Home', 'home'),
        ('Projects', 'projects'),
        ('Members', 'members')]


def view_init(request, session, tab):
    """Common init for all 'view' parts.

    Args:
        request: (Request)
        session: (DBSession)
        tab: (str) current tab in view

    Returns:
        (Team, dict of (str: any)): team, view_params
    """
    tid = request.matchdict['tid']
    team = Team.get(session, tid)
    if team is None:
        request.session.flash("Team %s does not exists" % tid, 'warning')
        raise HTTPFound(location=request.route_url('home'))

    current_uid = request.unauthenticated_userid

    # allow edition
    allow_edit = (current_uid is not None and
                  team_access_role(session, team, current_uid) == Role.edit)

    view_params = {"team": team,
                   "tabs": tabs,
                   "tab": tab,
                   "allow_edit": allow_edit,
                   "sections": []}

    return team, view_params


def edit_init(request, session, tab):
    """Common init for all 'edit' views.

    Args:
        request: (Request)
        session: (DBSession)
        tab: (str) current tab in view

    Returns:
        (Team, dict of (str: any)): team, view_params
    """
    team, view_params = view_init(request, session, tab)

    if not view_params["allow_edit"]:
        msg = "Access to %s edition not granted for you" % team.id
        request.session.flash(msg, 'warning')
        raise HTTPFound(location=request.route_url('home'))

    if 'back' in request.params:
        # request.session.flash("Edition stopped", 'success')
        loc = request.route_url('team_view_%s' % tab, tid=team.id)
        raise HTTPFound(location=loc)

    if "confirm_delete" in request.params:
        if remove_team(session, team):
            transaction.commit()
            request.session.flash("Team '%s' deleted" % team.id, 'success')
        else:
            request.session.flash("Failed to delete '%s'" % team.id, 'warning')
        raise HTTPFound(location=request.route_url('home'))

    return team, view_params
