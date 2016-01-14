from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from seeweb.models.auth import Role
from seeweb.models.user import User
from seeweb.views.user.tools import get_user

from .tools import edit_common, edit_init


@view_config(route_name='team_edit_members',
             renderer='templates/team/edit_members.jinja2')
def view(request):
    team, current_uid = edit_init(request)

    if 'back' in request.params:
        request.session.flash("Edition cancelled", 'success')
        return HTTPFound(location=request.route_url('team_view_members', tid=team.id))

    if 'default' in request.params:
        # reload default values for this user
        # actually already done
        pass
    elif 'update' in request.params:
        edit_common(request, team)

        # check for new members
        new_uid = request.params['new_member']
        if len(new_uid) > 0:
            user = get_user(request, new_uid)
            if not isinstance(user, User):
                return user

            # check user already in team
            if any(actor.user == new_uid for actor in team.auth):
                request.session.flash("%s already a member" % new_uid, 'warning')
            else:
                team.add_auth(user, 1)
                request.session.flash("New member %s added" % new_uid, 'success')

        # update user roles
        for actor in team.auth:
            new_role_str = request.params.get("role_%s" % actor.user, Role.denied)
            if new_role_str == "read":
                new_role = Role.read
            elif new_role_str == "edit":
                new_role = Role.edit
            else:
                new_role = Role.denied

            if new_role != actor.role:
                user = get_user(request, actor.user)
                if not isinstance(user, User):
                    return user

                team.update_auth(user, new_role)
    else:
        pass

    members = []

    for actor in team.auth:
        members.append((actor.role, actor.user))

    return {'team': team, 'tab': 'members', 'members': members}
