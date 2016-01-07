import os
import sys
import transaction
from pyramid.paster import get_appsettings, setup_logging
from pyramid.scripts.common import parse_vars
from sqlalchemy import engine_from_config
from ..models import Base, DBSession
# from seeweb.models.project import Project
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

        # pjts = {}
        users = {}

        # for i in range(5):
        #     name = "project%d" % i
        #     pjt = Project(name=name)
        #     session.add(pjt)
        #     pjts[name] = pjt

        for i in range(4):
            name = "user%d" % i
            usr = User(email="%s@gmail.com" % name, display_name=name)
            session.add(usr)
            users[name] = usr

        # usr = users['user0']
        # usr.projects.append(pjts['project0'])
        # usr.projects.append(pjts['project1'])
        #
        # usr = users['user1']
        # usr.projects.append(pjts['project1'])
        # usr.projects.append(pjts['project2'])
        #
        # usr = users['user2']
        # usr.projects.append(pjts['project3'])
        # usr.projects.append(pjts['project4'])
