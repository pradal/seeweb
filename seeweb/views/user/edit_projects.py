from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from seeweb.models import DBSession

from .tools import edit_common, edit_init, tabs


@view_config(route_name='user_edit_projects',
             renderer='templates/user/edit_projects.jinja2')
def view(request):
    session = DBSession()
    user, view_params = edit_init(request, session, 'projects')

    if 'back' in request.params:
        request.session.flash("Edition stopped", 'success')
        return HTTPFound(location=request.route_url('user_view_projects',
                                                    uid=user.id))

    if 'default' in request.params:
        # reload default values for this user
        # actually already done
        pass
    elif 'update' in request.params:
        edit_common(request, session, user)
    else:
        pass

    return view_params
