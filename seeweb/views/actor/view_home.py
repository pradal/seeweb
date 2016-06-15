from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.actor import Actor


@view_config(route_name='actor_view_home')
@view_config(route_name='actor_view_home_default')
def view(request):
    session = DBSession()
    uid = request.matchdict['uid']
    actor = Actor.get(session, uid)

    if actor is not None:
        if actor.type == "user":
            return HTTPFound(location=request.route_url('user_view_home', uid=uid))
        elif actor.type == "team":
            return HTTPFound(location=request.route_url('team_view_home', uid=uid))
        else:
            request.session.flash("Unknown actor type: %s" % actor.type, 'warning')
            raise HTTPFound(location=request.route_url('home'))

    request.session.flash("Actor %s does not exists" % uid, 'warning')
    raise HTTPFound(location=request.route_url('home'))
