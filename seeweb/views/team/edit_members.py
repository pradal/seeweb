from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.auth import Role
from seeweb.models.access import get_team, get_user, is_member

from .tools import edit_common, edit_init, tabs


def fetch_new_user(session, new_uid):
    user = get_user(session, new_uid)
    if user is None:
        user = get_team(session, new_uid)

    return user


def register_new_user(request, session, team, new_uid):
    user = fetch_new_user(session, new_uid)
    if user is None:
        request.session.flash("User %s does not exists" % new_uid, 'warning')
    else:
        # check user already in team
        if is_member(session, team, new_uid):
            request.session.flash("%s already a member" % new_uid, 'warning')
        else:
            role = Role.from_str(request.params.get("role_new", "denied"))
            if role == Role.denied:
                msg = "You granted 'denied' to %s, did nothing" % new_uid
                request.session.flash(msg, 'warning')
            else:
                team.add_auth(session, new_uid, role)
                request.session.flash("New member %s added" % user.id,
                                      'success')


@view_config(route_name='team_edit_members',
             renderer='templates/team/edit_members.jinja2')
def view(request):
    session = DBSession()
    team, current_uid = edit_init(request, session)

    if 'back' in request.params:
        request.session.flash("Edition cancelled", 'success')
        return HTTPFound(location=request.route_url('team_view_members',
                                                    tid=team.id))

    if 'default' in request.params:
        # reload default values for this team
        # actually already done
        pass
    elif 'update' in request.params:
        need_reload = edit_common(request, session, team)

        # check for new members
        new_uid = request.params['new_member']
        if len(new_uid) > 0:
            register_new_user(request, session, team, new_uid)
            need_reload = True

        # update user roles
        for actor in team.auth:
            if actor.user == new_uid:
                new_role_str = request.params.get("role_new", "denied")
            else:
                new_role_str = request.params.get("role_%s" % actor.user,
                                                  "denied")
            new_role = Role.from_str(new_role_str)

            if new_role != actor.role:
                team.update_auth(session, actor.user, new_role)
                need_reload = True

        if need_reload:
            loc = request.route_url('team_edit_members', tid=team.id)
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

    return {'team': team,
            "tabs": tabs,
            'tab': 'members',
            'members': members}
