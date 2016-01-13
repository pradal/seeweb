import os
import sys
import transaction
from pyramid.paster import get_appsettings, setup_logging
from pyramid.scripts.common import parse_vars
from sqlalchemy import engine_from_config

from seeweb.models import Base, DBSession
from seeweb.models.auth import add_auth, add_member, Role
from seeweb.models.project import Project
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

        add_member(team, users[0].id, Role.edit)
        add_member(team, users[1].id, Role.read)
        add_member(team, users[2].id, Role.read)

        projects = []

        for i in range(5):
            project = Project(id="pjt%d" % i,
                              owner=users[i % 4].id,
                              public=False)
            session.add(project)
            projects.append(project)

            users[i % 4].projects.append(project)

        projects[0].public = True
        add_auth(projects[0], users[2].id, Role.edit)
        add_auth(projects[4], users[2].id, Role.read)
