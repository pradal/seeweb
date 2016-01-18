import os
import sys
import transaction
from pyramid.paster import get_appsettings, setup_logging
from pyramid.scripts.common import parse_vars
from sqlalchemy import engine_from_config

from seeweb.models import Base, DBSession
from seeweb.models.auth import Role
from seeweb.models.edit import (create_comment,
                                create_project,
                                create_team,
                                create_user)


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
        users = [create_user(session,
                             uid='revesansparole',
                             name="Jerome Chopard",
                             email="revesansparole@gmail.com"),
                 create_user(session,
                             uid='pradal',
                             name="Christophe Pradal",
                             email="christophe.pradal@inria.fr"),
                 create_user(session,
                             uid='sartzet',
                             name="Simon Artzet",
                             email="simon.aertzet@inria.fr"),
                 create_user(session,
                             uid='fboudon',
                             name="Fred Boudon",
                             email="fred.boudon@inria.fr")]

        for i in range(4):
            users.append(create_user(session,
                                     uid='doofus%d' % i,
                                     name="Dummy Doofus",
                                     email="dummy.doofus@email.com"))

        # teams
        subsub_team = create_team(session, tid="subsubteam")
        subsub_team.description = """Test team only"""
        subsub_team.add_auth(session, 'doofus%d' % 0, Role.edit)

        sub_team = create_team(session, tid="subteam")
        sub_team.description = """Test team only"""
        sub_team.add_auth(session, 'doofus%d' % 1, Role.edit)
        sub_team.add_auth(session, "subsubteam", Role.edit, is_team=True)

        vplants = create_team(session, tid="vplants")
        vplants.description = """
Team
----
INRIA team based in Montpellier

        """

        vplants.add_auth(session, 'pradal', Role.edit)
        vplants.add_auth(session, 'fboudon', Role.read)

        oa = create_team(session, tid="openalea")
        oa.description = """
Community
---------

OpenAlea is an open source project primarily aimed at the plant research community.
It is a distributed collaborative effort to develop Python libraries and tools that address the needs of
current and future works in Plant Architecture modeling.
OpenAlea includes modules to analyse, visualize and model the functioning and growth of plant architecture.

        """

        oa.add_auth(session, 'revesansparole', Role.edit)
        oa.add_auth(session, 'pradal', Role.read)
        oa.add_auth(session, 'sartzet', Role.read)
        oa.add_auth(session, 'vplants', Role.edit, is_team=True)
        oa.add_auth(session, 'subteam', Role.edit, is_team=True)

        # projects
        projects = [create_project(session, 'revesansparole', name) for name in
                    ("pkglts",
                     "svgdraw",
                     "workflow")]

        for i in range(5):
            project = create_project(session, 'doofus%d' % i, "pjt%d" % i)
            projects.append(project)

        for i in range(3):
            projects[i].public = True

        projects[0].add_auth(session, 'sartzet', Role.edit)
        projects[1].add_auth(session, 'sartzet', Role.read)
        # projects[2].add_auth(session, 'openalea', Role.read, is_team=True)

        # comments
        pid = projects[0].id
        for i in range(4):
            create_comment(session,
                           pid,
                           users[i].id,
                           "very nasty comment (%d)" % i)
