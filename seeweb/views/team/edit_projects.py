from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from .tools import edit_common, edit_init


@view_config(route_name='team_edit_projects',
             renderer='templates/team/edit_projects.jinja2')
def view(request):
    team, current_uid = edit_init(request)

    if 'back' in request.params:
        request.session.flash("Edition cancelled", 'success')
        return HTTPFound(location=request.route_url('team_view_projects', tid=team.id))

    if 'default' in request.params:
        # reload default values for this user
        # actually already done
        pass
    elif 'update' in request.params:
        edit_common(request, team)
    else:
        pass

    return {'team': team, 'tab': 'projects'}
