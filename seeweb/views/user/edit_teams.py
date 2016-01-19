from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from seeweb.models import DBSession

from .tools import edit_common, edit_init, tabs


@view_config(route_name='user_edit_teams',
             renderer='templates/user/edit_teams.jinja2')
def view(request):
    session = DBSession()
    user, current_uid = edit_init(request, session)

    if 'back' in request.params:
        request.session.flash("Edition stopped", 'success')
        return HTTPFound(location=request.route_url('user_view_teams',
                                                    uid=user.id))

    if 'default' in request.params:
        # reload default values for this user
        # actually already done
        pass
    elif 'update' in request.params:
        edit_common(request, session, user)
    else:
        pass

    return {'user': user,
            "tabs": tabs,
            'tab': 'teams'}
