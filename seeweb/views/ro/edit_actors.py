from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.actor import Actor
from seeweb.models.auth import Role

from .commons import edit_init


def register_new_actor(request, session, ro, new_uid):
    """Register a new user according to info in form

    Args:
        request: (Request)
        session: (DBSession)
        ro: (ResearchObject)
        new_uid: (str) id of user to add to ro auth

    Returns:
        (bool): whether ro has changed and need to be reloaded
    """
    role = Role.from_str(request.params.get("role_new", "denied"))

    actor = Actor.get(session, new_uid)
    if actor is not None:
        if new_uid in (pol.actor for pol in ro.auth):
            msg = "%s already a direct member" % actor.id
            request.session.flash(msg, 'warning')
            return False

        ro.add_policy(session, actor, role)
        request.session.flash("New actor %s added" % actor.id, 'success')
        return True

    request.session.flash("Actor %s does not exists" % new_uid, 'warning')
    return False


@view_config(route_name='ro_edit_actors',
             renderer='templates/ro/edit_actors.jinja2')
def view(request):
    session = DBSession()
    ro, view_params = edit_init(request, session, 'actors')

    need_update = 'update' in request.params
    if not need_update:
        for pol in ro.auth:
            rm_button_id = "rm_%s" % pol.actor
            if rm_button_id in request.params:
                need_update = True

    if need_update:
        need_reload = False

        # check for new actors
        new_uid = request.params['new_actor']
        if len(new_uid) > 0:
            need_reload = register_new_actor(request, session, ro, new_uid)

        # update user roles
        for pol in ro.auth:
            # check need to remove
            if "rm_%s" % pol.actor in request.params:
                ro.remove_policy(session, pol.actor)
                request.session.flash("Actor %s removed" % pol.actor, 'success')
                need_reload = True
            else:  # update roles
                if pol.actor == new_uid and need_reload:
                    new_role_str = request.params.get("role_new", "denied")
                else:
                    new_role_str = request.params.get("role_%s" % pol.actor,
                                                      "denied")
                new_role = Role.from_str(new_role_str)

                if new_role != pol.role:
                    ro.update_policy(session, pol.actor, new_role)
                    need_reload = True

        if need_reload:
            loc = request.current_route_url()
            return HTTPFound(location=loc)
    else:
        pass

    actors = []
    for pol in ro.auth:
        actors.append(('user', pol.role, pol.actor))

    view_params["actors"] = actors

    return view_params
