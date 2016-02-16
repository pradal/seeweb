from glob import glob
import os
import sys
from PIL import Image
from pyramid.paster import get_appsettings, setup_logging
from pyramid.scripts.common import parse_vars
from sqlalchemy import engine_from_config
import transaction
from uuid import uuid1

from seeweb.avatar import upload_user_avatar
from seeweb.io import rmtree
from seeweb.models import Base, DBSession
from seeweb.models import installed  # used to create the associated table
from seeweb.models.auth import Role
from seeweb.model_edit import (create_comment,
                               create_executable,
                               create_notebook,
                               create_project,
                               create_team,
                               create_user,
                               create_workflow,
                               create_workflow_node,
                               add_project_auth,
                               add_team_auth,
                               add_dependency)
from seeweb.project.gallery import add_gallery_image


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)

    # create extra dirs
    for pth in ("data", "data/sessions", "../see_repo"):
        if not os.path.exists(pth):
            os.mkdir(pth)

    # remove sqlite file
    sqlite_pth = "data/seeweb.sqlite"
    if os.path.exists(sqlite_pth):
        os.remove(sqlite_pth)

    # clean data
    for obj_type in ("project", "team", "user"):
        for name in glob("seeweb/data/avatar/%s/*.png" % obj_type):
            try:
                os.remove(name)
            except OSError:
                print "unable to remove %s" % name

    for name in glob("seeweb/data/gallery/*/"):
        try:
            rmtree(name)
        except OSError:
            print "unable to remove %s" % name

    for name in glob("../see_repo/*/"):
        try:
            rmtree(name)
        except OSError:
            print "unable to remove %s" % name

    # setup config
    config_uri = argv[1]
    options = parse_vars(argv[2:])

    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)

    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)

    # populate database
    with transaction.manager:
        session = DBSession()

        # users
        doofus0 = create_user(session,
                              uid='doofus%d' % 0,
                              name="Dummy Doofus",
                              email="dummy.doofus@email.com")

        doofus1 = create_user(session,
                              uid='doofus%d' % 1,
                              name="Dummy Doofus",
                              email="dummy.doofus@email.com")

        doofus2 = create_user(session,
                              uid='doofus%d' % 2,
                              name="Dummy Doofus",
                              email="dummy.doofus@email.com")

        doofus3 = create_user(session,
                              uid='doofus%d' % 3,
                              name="Dummy Doofus",
                              email="dummy.doofus@email.com")

        revesansparole = create_user(session,
                                     uid='revesansparole',
                                     name="Jerome Chopard",
                                     email="revesansparole@gmail.com")
        img = Image.open("seeweb/scripts/avatar/revesansparole.png")
        upload_user_avatar(img, revesansparole)

        pradal = create_user(session,
                             uid='pradal',
                             name="Christophe Pradal",
                             email="christophe.pradal@inria.fr")
        img = Image.open("seeweb/scripts/avatar/pradal.png")
        upload_user_avatar(img, pradal)

        sartzet = create_user(session,
                              uid='sartzet',
                              name="Simon Artzet",
                              email="simon.aertzet@inria.fr")
        img = Image.open("seeweb/scripts/avatar/sartzet.png")
        upload_user_avatar(img, sartzet)

        fboudon = create_user(session,
                              uid='fboudon',
                              name="Fred Boudon",
                              email="fred.boudon@inria.fr")
        img = Image.open("seeweb/scripts/avatar/fboudon.png")
        upload_user_avatar(img, fboudon)

        for i in range(30):
            create_user(session,
                        uid="zzzz%d" % i,
                        name="John Doe%d" % i,
                        email="john%d@emil.com" % i)

        # teams
        subsub_team = create_team(session, tid="subsubteam")
        subsub_team.description = """Test team only"""
        add_team_auth(session, subsub_team, doofus0, Role.edit)

        sub_team = create_team(session, tid="subteam")
        sub_team.description = """Test team only"""
        add_team_auth(session, sub_team, doofus1, Role.edit)
        add_team_auth(session, sub_team, subsub_team, Role.edit)

        vplants = create_team(session, tid="vplants")
        vplants.description = """
Team
----
INRIA team based in Montpellier

        """

        add_team_auth(session, vplants, pradal, Role.edit)
        add_team_auth(session, vplants, fboudon, Role.view)

        oa = create_team(session, tid="openalea")
        oa.description = """
Community
---------

OpenAlea is an open source project primarily aimed at the plant research community.
It is a distributed collaborative effort to develop Python libraries and tools that address the needs of
current and future works in Plant Architecture modeling.
OpenAlea includes modules to analyse, visualize and model the functioning and growth of plant architecture.

        """

        add_team_auth(session, oa, revesansparole, Role.edit)
        add_team_auth(session, oa, pradal, Role.view)
        add_team_auth(session, oa, sartzet, Role.view)
        add_team_auth(session, oa, vplants, Role.edit)
        add_team_auth(session, oa, sub_team, Role.edit)

        # projects
        pkglts = create_project(session, 'revesansparole', 'pkglts')
        pkglts.public = True
        pkglts.doc_url = "http://pkglts.readthedocs.org/en/latest/"
        pkglts.src_url = " C:/Users/jerome/Desktop/pkglts/.git"
        pkglts.store_description("""
This project is part of OpenAlea_.

.. image:: http://localhost:6543/avatar/team/openalea_small.png
    :alt: Openalea team
    :target: http://localhost:6543/team/openalea

.. _OpenAlea: http://localhost:6543/team/openalea

        """)
        add_project_auth(session, pkglts, sartzet, Role.edit)
        for img_name in ["Chrysanthemum.png",
                         "Desert.png",
                         "Jellyfish.png",
                         "Koala.png",
                         "Penguins.png"]:
            img = Image.open("seeweb/scripts/gallery/%s" % img_name)
            add_gallery_image(pkglts, img, img_name)

        svgdraw = create_project(session, 'revesansparole', 'svgdraw')
        svgdraw.public = True
        svgdraw.src_url = "https://github.com/revesansparole/svgdraw.git"
        add_project_auth(session, svgdraw, sartzet, Role.view)

        workflow = create_project(session, 'revesansparole', 'workflow')
        workflow.public = True
        add_project_auth(session, workflow, oa, Role.view)
        for i in range(5):
            create_executable(session, workflow, "executable%d" % i)

        for i in range(5):
            create_notebook(session, workflow, "notebook%d" % i)

        ndefs = []

        for i in range(3):
            node_def = dict(id=uuid1().hex,
                            name="read%d" % i,
                            category="oanode",
                            description="toto was here",
                            author="revesansparole",
                            function="testio:read",
                            inputs=[dict(name="in1", interface="IInt",
                                         value="0", descr="counter"),
                                    dict(name="in2", interface="IStr",
                                         value="a", descr="unit")],
                            outputs=[dict(name="ret", interface="IInt",
                                          descr="important result")])

            create_workflow_node(session, workflow, node_def)
            ndefs.append(node_def)

        workflow_def = dict(id=uuid1().hex,
                            name="sample_workflow",
                            category="oaworkflow",
                            description="trying some stuff",
                            author="revesansparole",
                            nodes=[dict(id=ndefs[0]['id'], label="node1",
                                        x=100, y=10),
                                   dict(id=ndefs[1]['id'], label=None,
                                        x=200, y=10),
                                   dict(id=ndefs[2]['id'], label=None,
                                        x=150, y=100),
                                   dict(id=uuid1().hex, label="fail",
                                        x=150, y=200)],
                            connections=[(0, "ret", 2, "in1"),
                                         (1, "ret", 2, "in2"),
                                         (2, "ret", 3, "in")])

        create_workflow(session, workflow, workflow_def)

        spl = create_project(session, 'revesansparole', 'sample_project')
        spl.public = True
        spl.src_url = "C:/Users/jerome/Desktop/see/sample_project/.git"
        add_dependency(session, spl, "numpy", "1.0")
        add_dependency(session, spl, "pkglts", "1.0")

        for i in range(5):
            create_project(session, 'doofus%d' % i, "stoopid%d" % i)

        # comments
        for i in range(4):
            create_comment(session,
                           'pkglts',
                           "doofus%d" % i,
                           "very nasty comment (%d)" % i)
