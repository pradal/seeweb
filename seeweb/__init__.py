from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from models import DBSession, Base


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.include('pyramid_beaker')
    config.add_static_view('static', 'static', cache_max_age=3600)

    # public
    config.add_route('home', '/')
    config.add_route('project_list', 'projects')
    config.add_route('user_list', 'users')
    config.add_route('team_list', 'teams')

    # admin
    config.add_route('admin_users', "admin/users")
    config.add_route('admin_projects', "admin/projects")

    # user auth
    config.add_route('user_login', 'user_login')
    config.add_route('user_logout', 'user_logout')
    config.add_route('user_register', 'user_register')

    # edit
    config.add_route('team_edit', 'team/{tid}/edit')
    config.add_route('project_edit', '{uid}/{pid}/edit')
    config.add_route('user_edit', '{uid}/edit')

    # display
    config.add_route('team_view_home', 'team/{tid}/home')
    config.add_route('team_view_projects', 'team/{tid}/projects')
    config.add_route('team_view_members', 'team/{tid}/members')
    config.add_route('team_view_home_default', 'team/{tid}')
    config.add_route('user_view_home', 'user/{uid}/home')
    config.add_route('user_view_projects', 'user/{uid}/projects')
    config.add_route('user_view_teams', 'user/{uid}/teams')
    config.add_route('user_view_home_default', 'user/{uid}')
    config.add_route('project_home', '{uid}/{pid}')

    config.scan()

    return config.make_wsgi_app()
