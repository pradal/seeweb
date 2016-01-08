from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.user import User


@view_config(route_name='user_edit',
             renderer='templates/admin/user_edit.jinja2')
def view(request):
    if 'cancel' in request.params:
        request.session.flash("New user cancelled", 'success')
        return HTTPFound(location=request.route_url('users_admin'))

    uid = request.matchdict['uid']
    session = DBSession()

    if uid == 'None':
        # new user
        usr = User(email="dupond@example.com", display_name="Jeannot")
        create = True
    elif 'save_new' in request.params:
        # edit user display_name
        display_name = request.params['display_name']
        if len(display_name) == 0:
            request.session.flash("No display name", 'warning')
            return HTTPFound(location=request.route_url('users_admin'))

        # edit user email
        # TODO: check unity and flash/rollback
        email = request.params['email']
        if len(email) == 0:
            request.session.flash("No email", 'warning')
            return HTTPFound(location=request.route_url('users_admin'))

        usr = User(email=email, display_name=display_name)
        session.add(usr)
        create = False

    else:
        usr = session.query(User).filter(User.email == uid).one()
        create = False

        if 'default' in request.params:
            # reload default values for this user
            # actually does nothing
            pass
        elif 'delete' in request.params:
            session.delete(usr)
            request.session.flash("User %s deleted" % usr.display_name,
                                  'success')
            return HTTPFound(location=request.route_url('users_admin'))
        elif 'update' in request.params:
            # edit user display_name
            display_name = request.params['display_name']
            if len(display_name) > 0:
                usr.display_name = display_name

            # edit user email
            # TODO: check unity and flash/rollback
            email = request.params['email']
            if len(email) > 0:
                usr.email = email
        else:
            pass

    return {'user': usr, 'create': create}
