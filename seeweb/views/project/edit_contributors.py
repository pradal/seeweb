from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.auth import Role
from seeweb.models.access import get_team, get_user

from .tools import edit_common, edit_init, tabs


def register_new_user(request, session, project, new_uid):
    role = Role.from_str(request.params.get("role_new", "denied"))
    if role == Role.denied:
        msg = "You granted 'denied' to %s, did nothing" % new_uid
        request.session.flash(msg, 'warning')
        return False

    user = get_user(session, new_uid)
    if user is not None:
        if project.get_actor(new_uid) is not None:
            request.session.flash("%s already a member" % new_uid, 'warning')
            return False

        project.add_auth(session, new_uid, role)
        request.session.flash("New member %s added" % user.id, 'success')
        return True

    team = get_team(session, new_uid)
    if team is not None:
        if project.get_actor(new_uid) is not None:
            request.session.flash("%s already a member" % new_uid, 'warning')
            return False

        project.add_auth(session, new_uid, role, is_team=True)
        request.session.flash("New member %s added" % new_uid, 'success')
        return True

    request.session.flash("User %s does not exists" % new_uid, 'warning')
    return False


@view_config(route_name='project_edit_contributors',
             renderer='templates/project/edit_contributors.jinja2')
def view(request):
    session = DBSession()
    project, allow_edit = edit_init(request, session)

    if 'back' in request.params:
        request.session.flash("Edition stopped", 'success')
        loc = request.route_url('project_view_contributors', pid=project.id)
        return HTTPFound(location=loc)

    if 'default' in request.params:
        # reload default values for this user
        # actually already done
        pass
    elif 'update' in request.params:
        need_reload = edit_common(request, session, project)

        # check for new members
        new_uid = request.params['new_member']
        if len(new_uid) > 0:
            need_reload = register_new_user(request, session, project, new_uid)

        # update user roles
        for actor in project.auth:
            if actor.user == new_uid and need_reload:
                new_role_str = request.params.get("role_new", "denied")
            else:
                new_role_str = request.params.get("role_%s" % actor.user,
                                                  "denied")
            new_role = Role.from_str(new_role_str)

            if new_role != actor.role:
                project.update_auth(session, actor.user, new_role)
                need_reload = True

        if need_reload:
            loc = request.route_url('project_edit_contributors', pid=project.id)
            return HTTPFound(location=loc)
    else:
        pass

    members = []
    for actor in project.auth:
        if actor.is_team:
            typ = 'team'
        else:
            typ = 'user'
        members.append((typ, actor.role, actor.user))

    return {"project": project,
            "tabs": tabs,
            "tab": 'contributors',
            "members": members}
