from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from models import DBSession, Base
from views.project.tools import tabs as project_tabs
from views.team.tools import tabs as team_tabs
from views.user.tools import tabs as user_tabs


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.include('pyramid_beaker')
    config.add_static_view(name='static', path='static', cache_max_age=3600)
    config.add_static_view(name='avatar', path='avatar', cache_max_age=3600)

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

    # comment
    config.add_route('comment_edit_new', 'comment/new')
    config.add_route('comment_edit_rating', 'comment/{cid}/rate/{vote}')

    # project
    for tab_title, tab_id in project_tabs:
        config.add_route('project_edit_%s' % tab_id, 'project/{pid}/edit/%s' % tab_id)
        config.add_route('project_view_%s' % tab_id, 'project/{pid}/%s' % tab_id)

    config.add_route('project_view_home_default', 'project/{pid}')

    # team
    for tab_title, tab_id in team_tabs:
        config.add_route('team_edit_%s' % tab_id, 'team/{tid}/edit/%s' % tab_id)
        config.add_route('team_view_%s' % tab_id, 'team/{tid}/%s' % tab_id)

    config.add_route('team_view_home_default', 'team/{tid}')

    # user
    for tab_title, tab_id in user_tabs:
        config.add_route('user_edit_%s' % tab_id, 'user/{uid}/edit/%s' % tab_id)
        config.add_route('user_view_%s' % tab_id, 'user/{uid}/%s' % tab_id)

    config.add_route('user_view_home_default', 'user/{uid}')

    config.scan()

    return config.make_wsgi_app()
