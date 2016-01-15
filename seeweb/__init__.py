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
    config.add_route('admin_teams', "admin/teams")
    config.add_route('admin_projects', "admin/projects")
    config.add_route('admin_comments', "admin/comments")

    # user auth
    config.add_route('user_login', 'user_login')
    config.add_route('user_logout', 'user_logout')
    config.add_route('user_register', 'user_register')

    # edit
    config.add_route('team_edit_home', 'team/{tid}/edit/home')
    config.add_route('team_edit_projects', 'team/{tid}/edit/projects')
    config.add_route('team_edit_members', 'team/{tid}/edit/members')
    config.add_route('user_edit_home', 'user/{uid}/edit/home')
    config.add_route('user_edit_projects', 'user/{uid}/edit/projects')
    config.add_route('user_edit_teams', 'user/{uid}/edit/teams')
    config.add_route('project_edit', 'project/{pid}/edit')

    # comment
    config.add_route('comment_edit_rating', 'comment/{cid}/rate/{vote}')

    # display
    config.add_route('team_view_home', 'team/{tid}/home')
    config.add_route('team_view_projects', 'team/{tid}/projects')
    config.add_route('team_view_members', 'team/{tid}/members')
    config.add_route('team_view_home_default', 'team/{tid}')

    config.add_route('user_view_home', 'user/{uid}/home')
    config.add_route('user_view_projects', 'user/{uid}/projects')
    config.add_route('user_view_teams', 'user/{uid}/teams')
    config.add_route('user_view_home_default', 'user/{uid}')

    config.add_route('project_view_home', 'project/{pid}/home')
    config.add_route('project_view_documentation', 'project/{pid}/doc')
    config.add_route('project_view_source', 'project/{pid}/source')
    config.add_route('project_view_contributors', 'project/{pid}/contributors')
    config.add_route('project_view_comments', 'project/{pid}/comments')
    config.add_route('project_view_home_default', 'project/{pid}')

    config.scan()

    return config.make_wsgi_app()
