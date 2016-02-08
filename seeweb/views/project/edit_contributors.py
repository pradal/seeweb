from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.auth import Role
from seeweb.model_access import get_team, get_user
from seeweb.model_edit import add_project_auth, remove_auth, update_auth

from .commons import edit_init


def register_new_user(request, session, project, new_uid):
    """Register a new user according to info in form

    Args:
        request: (Request)
        session: (DBSession)
        project: (Project)
        new_uid: (str) id of user to add to project auth

    Returns:
        (bool): whether project has changed and need to be reloaded
    """
    role = Role.from_str(request.params.get("role_new", "denied"))

    user = get_user(session, new_uid)
    if user is not None:
        if project.get_actor(new_uid) is not None:
            request.session.flash("%s already a member" % new_uid, 'warning')
            return False

        add_project_auth(session, project, user, role)
        request.session.flash("New member %s added" % new_uid, 'success')
        return True

    team = get_team(session, new_uid)
    if team is not None:
        if project.get_actor(new_uid) is not None:
            request.session.flash("%s already a member" % new_uid, 'warning')
            return False

        add_project_auth(session, project, team, role)
        request.session.flash("New member %s added" % new_uid, 'success')
        return True

    request.session.flash("User %s does not exists" % new_uid, 'warning')
    return False


@view_config(route_name='project_edit_contributors',
             renderer='templates/project/edit_contributors.jinja2')
def view(request):
    session = DBSession()
    project, view_params = edit_init(request, session, 'contributors')

    need_update = 'update' in request.params
    if not need_update:
        for actor in project.auth:
            rm_button_id = "rm_%s" % actor.user
            if rm_button_id in request.params:
                need_update = True

    if need_update:
        need_reload = False

        # check for new members
        new_uid = request.params['new_member']
        if len(new_uid) > 0:
            need_reload = register_new_user(request, session, project, new_uid)

        # update user roles
        for actor in project.auth:
            # check need to remove
            if "rm_%s" % actor.user in request.params:
                remove_auth(session, project, actor.user)
                request.session.flash("User %s removed" % actor.user, 'success')
                need_reload = True
            else:
                if actor.user == new_uid and need_reload:
                    new_role_str = request.params.get("role_new", "denied")
                else:
                    new_role_str = request.params.get("role_%s" % actor.user,
                                                      "denied")
                new_role = Role.from_str(new_role_str)

                if new_role != actor.role:
                    update_auth(session, project, actor.user, new_role)
                    need_reload = True

        if need_reload:
            loc = request.current_route_url()
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

    view_params["members"] = members

    return view_params
