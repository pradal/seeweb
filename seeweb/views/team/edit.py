from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from seeweb.views.tools import get_current_uid

from .tools import get_team


@view_config(route_name='team_edit',
             renderer='templates/team/edit.jinja2')
def view(request):
    tid = request.matchdict['tid']
    current_uid = get_current_uid(request)

    team = get_team(request, tid)

    if not team.public:
        request.session.flash("Access to %s edition not granted for you" % tid,
                              'warning')
        return HTTPFound(location=request.route_url('home'))

    # if 'cancel' in request.params:
    #     request.session.flash("Edition cancelled", 'success')
    #     return HTTPFound(location=request.route_url('user_home', uid=uid))

    # if 'default' in request.params:
    #     # reload default values for this user
    #     # actually already done
    #     pass
    # elif 'update' in request.params:
    #     # edit user display_name
    #     name = request.params['name']
    #     if len(name) > 0:
    #         user.name = name
    #
    #     # edit user email
    #     # TODO: check validity and flash/rollback
    #     email = request.params['email']
    #     if len(email) > 0:
    #         user.email = email
    # else:
    #     pass

    return {'team': team}
