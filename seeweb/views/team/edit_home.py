from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from .tools import edit_common, edit_init


@view_config(route_name='team_edit_home',
             renderer='templates/team/edit_home.jinja2')
def view(request):
    team, current_uid = edit_init(request)

    if 'back' in request.params:
        request.session.flash("Edition cancelled", 'success')
        return HTTPFound(location=request.route_url('team_view_home', tid=team.id))

    if 'default' in request.params:
        # reload default values for this user
        # actually already done
        pass
    elif 'update' in request.params:
        edit_common(request, team)

        if 'description' in request.params:
            # sanitize
            team.description = request.params['description']
    else:
        pass

    return {'team': team, 'tab': 'home'}
