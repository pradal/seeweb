from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.auth import Role
from seeweb.models.team import Team
from seeweb.models.user import User

from .commons import edit_init


def register_new_user(request, session, team, new_uid):
    """Register a new user according to info in form

    Args:
        request: (Request)
        session: (DBSession)
        team: (Team)
        new_uid: (str) id of user to add to team auth

    Returns:
        (bool): whether team has changed and need to be reloaded
    """
    if new_uid == team.id:
        msg = "Cannot be a member of itself"
        request.session.flash(msg, 'warning')
        return False

    role = Role.from_str(request.params.get("role_new", "denied"))

    member = User.get(session, new_uid)
    if member is not None:
        if team.get_actor(new_uid) is not None:
            request.session.flash("%s already a member" % member.id, 'warning')
            return False

        team.add_auth(session, member, role)
        request.session.flash("New member %s added" % member.id, 'success')
        return True

    member = Team.get(session, new_uid)
    if member is not None:
        if team.has_member(session, new_uid):
            request.session.flash("%s already a member" % member.id, 'warning')
            return False

        if member.has_member(session, team.id):
            msg = "Circular reference %s is a member of %s" % (team.id,
                                                               member.id)
            request.session.flash(msg, 'warning')
            return False

        team.add_auth(session, member, role)
        request.session.flash("New member %s added" % member.id, 'success')
        return True

    request.session.flash("User %s does not exists" % new_uid, 'warning')
    return False


@view_config(route_name='team_edit_members',
             renderer='templates/team/edit_members.jinja2')
def view(request):
    session = DBSession()
    team, view_params = edit_init(request, session, 'members')

    need_update = 'update' in request.params
    if not need_update:
        for actor in team.auth:
            rm_button_id = "rm_%s" % actor.user
            if rm_button_id in request.params:
                need_update = True

    if need_update:
        need_reload = False

        # check for new members
        new_uid = request.params['new_member']
        if len(new_uid) > 0:
            need_reload = register_new_user(request, session, team, new_uid)

        # update user roles
        for actor in team.auth:
            # check need to remove
            if "rm_%s" % actor.user in request.params:
                team.remove_auth(session, actor.user)
                request.session.flash("User %s removed" % actor.user, 'success')
                need_reload = True
            else:  # update roles
                if actor.user == new_uid and need_reload:
                    new_role_str = request.params.get("role_new", "denied")
                else:
                    new_role_str = request.params.get("role_%s" % actor.user,
                                                      "denied")
                new_role = Role.from_str(new_role_str)

                if new_role != actor.role:
                    team.update_auth(session, actor.user, new_role)
                    need_reload = True

        if need_reload:
            loc = request.current_route_url()
            return HTTPFound(location=loc)
    else:
        pass

    members = []

    for actor in team.auth:
        if actor.is_team:
            typ = 'team'
        else:
            typ = 'user'
        members.append((typ, actor.role, actor.user))

    view_params["members"] = members

    return view_params
