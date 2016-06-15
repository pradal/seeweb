from pyramid.authentication import SessionAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from pyramid.httpexceptions import HTTPFound
from sqlalchemy import engine_from_config

from models import DBSession, Base
from views.ro.commons import tabs as ro_tabs
from views.team.commons import tabs as team_tabs
from views.user.commons import tabs as user_tabs
#
from .security import groupfinder


def forbidden(request):
    """Simple view for access to forbidden zones.

    Automatically called by pyramid framework

    Args:
        request: (Request)

    Returns:
        (HTTPFound)
    """
    request.session.flash("Access forbidden", 'warning')
    return HTTPFound(location=request.route_url('home'))


def main(global_config, **settings):
    """This function returns a Pyramid WSGI application.

    Args:
        global_config: (dict) config parameters
        **settings: (dict) extra settings

    Returns:
        (WSGI app)
    """
    del global_config
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    config = Configurator(settings=settings,
                          root_factory='seeweb.models.RootFactory')
    config.include('pyramid_jinja2')
    config.include('pyramid_beaker')

    # Security policies
    authn_policy = SessionAuthenticationPolicy(callback=groupfinder)
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.add_forbidden_view(forbidden)

    # static
    config.add_static_view(name='static', path='static', cache_max_age=3600)

    config.add_static_view(name='avatar',
                           path="seeweb:data/avatar",
                           cache_max_age=3600)
    config.add_static_view(name='gallery',
                           path="seeweb:data/gallery",
                           cache_max_age=3600)

    # public
    config.add_route('home', '/')
    config.add_route('documentation', 'documentation')
    config.add_route('user_list', 'users')
    config.add_route('team_list', 'teams')
    config.add_route('ro_list', 'ros')

    # admin
    config.add_route('admin_users', "admin/users")
    config.add_route('admin_teams', "admin/teams")
    config.add_route('admin_ros', "admin/ros")

    # # user auth
    config.add_route('user_login', 'user_login')
    config.add_route('user_logout', 'user_logout')
    config.add_route('user_register', 'user_register')

    # actor
    config.add_route('actor_view_home', 'actor/{uid}/home')
    config.add_route('actor_view_home_default', 'actor/{uid}')

    # team
    for tab_title, tab_id in team_tabs:
        config.add_route('team_edit_%s' % tab_id, 'team/{uid}/edit/%s' % tab_id)
        config.add_route('team_view_%s' % tab_id, 'team/{uid}/%s' % tab_id)

    config.add_route('team_view_home_default', 'team/{uid}')

    # user
    for tab_title, tab_id in user_tabs:
        config.add_route('user_edit_%s' % tab_id, 'user/{uid}/edit/%s' % tab_id)
        config.add_route('user_view_%s' % tab_id, 'user/{uid}/%s' % tab_id)

    config.add_route('user_view_home_default', 'user/{uid}')

    # research objects
    for tab_title, tab_id in ro_tabs:
        config.add_route('ro_edit_%s' % tab_id, 'ro/{uid}/edit/%s' % tab_id)
        config.add_route('ro_view_%s' % tab_id, 'ro/{uid}/%s' % tab_id)

    config.add_route('ro_view_home_default', 'ro/{uid}')

    config.add_route('ro_container_view', 'ro_container/{uid}')

    config.scan()

    return config.make_wsgi_app()
