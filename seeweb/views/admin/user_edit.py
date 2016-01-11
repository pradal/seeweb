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

    user = session.query(User).filter(User.username == uid).one()

    if 'default' in request.params:
        # reload default values for this user
        # actually already done
        pass
    elif 'delete' in request.params:
        session.delete(user)
        request.session.flash("User %s deleted" % user.username,
                              'success')
        return HTTPFound(location=request.route_url('users_admin'))
    elif 'update' in request.params:
        # edit user display_name
        name = request.params['name']
        if len(name) > 0:
            user.name = name

        # edit user email
        # TODO: check validity and flash/rollback
        email = request.params['email']
        if len(email) > 0:
            user.email = email
    else:
        pass

    return {'user': user}
