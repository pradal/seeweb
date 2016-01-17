import os
import sys
import transaction
from pyramid.paster import get_appsettings, setup_logging
from pyramid.scripts.common import parse_vars
from sqlalchemy import engine_from_config

from seeweb.models import Base, DBSession
from seeweb.models.auth import Role
from seeweb.models.edit import create_comment, create_project
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

    # remove sqlite file
    sqlite_pth = "data/seeweb.sqlite"
    if os.path.exists(sqlite_pth):
        os.remove(sqlite_pth)

    config_uri = argv[1]
    options = parse_vars(argv[2:])

    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)

    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)

    with transaction.manager:
        session = DBSession()

        # users
        users = [User(id='revesansparole',
                      name="Jerome Chopard",
                      email="revesansparole@gmail.com"),
                 User(id='pradal',
                      name="Christophe Pradal",
                      email="christophe.pradal@inria.fr"),
                 User(id='sartzet',
                      name="Simon Artzet",
                      email="simon.aertzet@inria.fr"),
                 User(id='fboudon',
                      name="Fred Boudon",
                      email="fred.boudon@inria.fr")]

        for i in range(4):
            users.append(User(id='doofus%d' % i,
                              name="Dummy Doofus",
                              email="dummy.doofus@email.com"))

        for user in users:
            session.add(user)

        # teams
        subsub_team = Team(id="subsubteam")
        subsub_team.description = """Test team only"""
        session.add(subsub_team)
        subsub_team.add_auth(Role.edit, user=users[4])

        sub_team = Team(id="subteam")
        sub_team.description = """Test team only"""
        session.add(sub_team)
        sub_team.add_auth(Role.edit, user=users[5])
        sub_team.add_auth(Role.edit, team=subsub_team)

        vplants = Team(id="vplants")
        vplants.description = """
Team
----
INRIA team based in Montpellier

        """
        session.add(vplants)

        vplants.add_auth(Role.edit, user=users[1])
        vplants.add_auth(Role.read, user=users[3])

        oa = Team(id="openalea")
        oa.description = """
Community
---------

OpenAlea is an open source project primarily aimed at the plant research community.
It is a distributed collaborative effort to develop Python libraries and tools that address the needs of
current and future works in Plant Architecture modeling.
OpenAlea includes modules to analyse, visualize and model the functioning and growth of plant architecture.

        """
        session.add(oa)

        oa.add_auth(Role.edit, user=users[0])
        oa.add_auth(Role.read, user=users[1])
        oa.add_auth(Role.read, user=users[2])
        oa.add_auth(Role.edit, team=vplants)
        oa.add_auth(Role.read, team=sub_team)

        # projects
        projects = [create_project(users[0], name) for name in ("pkglts",
                                                                "svgdraw",
                                                                "workflow")]

        for i in range(5):
            project = create_project(users[i], "pjt%d" % i)
            projects.append(project)

        for project in projects:
            session.add(project)

        for i in range(3):
            projects[i].public = True

        projects[0].add_auth(users[2].id, Role.edit)
        projects[1].add_auth(users[2].id, Role.read)
        # projects[2].add_auth(openalea.id, Role.read)

        # comments
        pid = projects[0].id
        for i in range(4):
            cmt = create_comment(pid, users[i].id, "very nasty comment (%d)" % i)
            session.add(cmt)
