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

    # admin
    config.add_route('users_admin', "admin/users")
    config.add_route('user_edit', "admin/user/{uid}")
    config.add_route('projects_admin', "admin/projects")

    # project

    # user
    config.add_route('user_login', 'user_login')
    config.add_route('user_logout', 'user_logout')
    config.add_route('user_register', 'user_register')

    # specific routes
    config.add_route('project_home', '{uid}/{pid}')
    config.add_route('user_home', '{uid}')

    config.scan()

    return config.make_wsgi_app()
