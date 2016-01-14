import os
import sys
import transaction
from pyramid.paster import get_appsettings, setup_logging
from pyramid.scripts.common import parse_vars
from sqlalchemy import engine_from_config

from seeweb.models import Base, DBSession
from seeweb.models.auth import Role
from seeweb.models.edit import create_project
from seeweb.models.team import Team
from seeweb.models.user import User


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)

    config_uri = argv[1]
    options = parse_vars(argv[2:])

    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)

    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)

    with transaction.manager:
        session = DBSession()

        users = []

        for i in range(4):
            user = User(id="user%d" % i)
            session.add(user)
            users.append(user)

        team = Team(id="openalea", public=True)
        session.add(team)

        team.add_auth(users[0], Role.edit)
        team.add_auth(users[1], Role.read)
        team.add_auth(users[2], Role.read)

        projects = []

        for i in range(5):
            project = create_project(users[i % 4], "pjt%d" % i)
            session.add(project)
            projects.append(project)

        projects[0].public = True
        projects[0].add_auth(users[2].id, Role.edit)
        projects[4].add_auth(users[2].id, Role.read)
