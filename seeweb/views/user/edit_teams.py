from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from .tools import edit_common, edit_init


@view_config(route_name='user_edit_teams',
             renderer='templates/user/edit_teams.jinja2')
def view(request):
    user, current_uid = edit_init(request)
    if user is None:
        return current_uid

    if 'back' in request.params:
        request.session.flash("Edition cancelled", 'success')
        return HTTPFound(location=request.route_url('user_view_teams', uid=user.id))

    if 'default' in request.params:
        # reload default values for this user
        # actually already done
        pass
    elif 'update' in request.params:
        edit_common(request, user)
    else:
        pass

    return {'user': user, 'tab': 'teams'}
