from glob import glob
import os
import sys
from PIL import Image
from pyramid.paster import get_appsettings, setup_logging
from pyramid.scripts.common import parse_vars
from sqlalchemy import engine_from_config
import transaction
from uuid import uuid1

from seeweb.avatar import upload_team_avatar, upload_user_avatar
from seeweb.io import rmtree
from seeweb.models import Base, DBSession
from seeweb.models import installed  # used to create the associated table
from seeweb.models.auth import Role
from seeweb.models.comment import Comment
from seeweb.models.content_item import ContentItem
from seeweb.models.team import Team
from seeweb.models.project import Project
from seeweb.models.user import User
from seeweb.project.gallery import add_gallery_image

import pjt_scene3d
import pjt_workflow


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
        doofus0 = User.create(session,
                              uid='doofus%d' % 0,
                              name="Dummy Doofus",
                              email="dummy.doofus@email.com")

        doofus1 = User.create(session,
                              uid='doofus%d' % 1,
                              name="Dummy Doofus",
                              email="dummy.doofus@email.com")

        doofus2 = User.create(session,
                              uid='doofus%d' % 2,
                              name="Dummy Doofus",
                              email="dummy.doofus@email.com")

        doofus3 = User.create(session,
                              uid='doofus%d' % 3,
                              name="Dummy Doofus",
                              email="dummy.doofus@email.com")

        revesansparole = User.create(session,
                                     uid='revesansparole',
                                     name="Jerome Chopard",
                                     email="revesansparole@gmail.com")
        img = Image.open("seeweb/scripts/avatar/revesansparole.png")
        upload_user_avatar(img, revesansparole)

        pradal = User.create(session,
                             uid='pradal',
                             name="Christophe Pradal",
                             email="christophe.pradal@inria.fr")
        img = Image.open("seeweb/scripts/avatar/pradal.png")
        upload_user_avatar(img, pradal)

        sartzet = User.create(session,
                              uid='sartzet',
                              name="Simon Artzet",
                              email="simon.aertzet@inria.fr")
        img = Image.open("seeweb/scripts/avatar/sartzet.png")
        upload_user_avatar(img, sartzet)

        fboudon = User.create(session,
                              uid='fboudon',
                              name="Fred Boudon",
                              email="fred.boudon@inria.fr")
        img = Image.open("seeweb/scripts/avatar/fboudon.png")
        upload_user_avatar(img, fboudon)

        for i in range(30):
            User.create(session,
                        uid="zzzz%d" % i,
                        name="John Doe%d" % i,
                        email="john%d@emil.com" % i)

        # teams
        subsub_team = Team.create(session, tid="subsubteam")
        subsub_team.description = """Test team only"""
        subsub_team.add_auth(session, doofus0, Role.edit)

        sub_team = Team.create(session, tid="subteam")
        sub_team.description = """Test team only"""
        sub_team.add_auth(session, doofus1, Role.edit)
        sub_team.add_auth(session, subsub_team, Role.edit)

        vplants = Team.create(session, tid="vplants")
        img = Image.open("seeweb/scripts/avatar/vplants.png")
        upload_team_avatar(img, vplants)
        vplants.description = """
Team
----
INRIA team based in Montpellier

        """

        vplants.add_auth(session, pradal, Role.edit)
        vplants.add_auth(session, fboudon, Role.view)

        oa = Team.create(session, tid="openalea")
        img = Image.open("seeweb/scripts/avatar/openalea.png")
        upload_team_avatar(img, oa)
        oa.description = """
Community
---------

OpenAlea is an open source project primarily aimed at the plant research community.
It is a distributed collaborative effort to develop Python libraries and tools that address the needs of
current and future works in Plant Architecture modeling.
OpenAlea includes modules to analyse, visualize and model the functioning and growth of plant architecture.

        """

        oa.add_auth(session, revesansparole, Role.edit)
        oa.add_auth(session, pradal, Role.view)
        oa.add_auth(session, sartzet, Role.view)
        oa.add_auth(session, vplants, Role.edit)
        oa.add_auth(session, sub_team, Role.edit)

        # projects
        for i in range(5):
            Project.create(session, 'doofus%d' % i, "stoopid%d" % i)

        pkglts = Project.create(session, 'revesansparole', 'pkglts')
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
        pkglts.add_auth(session, sartzet, Role.edit)
        for img_name in ["Chrysanthemum.png",
                         "Desert.png",
                         "Jellyfish.png",
                         "Koala.png",
                         "Penguins.png"]:
            img = Image.open("seeweb/scripts/gallery/%s" % img_name)
            add_gallery_image(pkglts, img, img_name)

        # comments
        for i in range(4):
            Comment.create(session,
                           'pkglts',
                           "doofus%d" % i,
                           "very nasty comment (%d)" % i)

        svgdraw = Project.create(session, 'revesansparole', 'svgdraw')
        svgdraw.public = True
        svgdraw.src_url = "https://github.com/revesansparole/svgdraw.git"
        svgdraw.add_auth(session, sartzet, Role.view)

        notebook = Project.create(session, 'revesansparole', 'notebook_pjt')
        notebook.public = True
        for i in range(5):
            item = ContentItem.create(session, uuid1().hex, "executable",
                                      notebook)
            item.name = "executable%d" % i

        for i in range(5):
            item = ContentItem.create(session, uuid1().hex, "notebook",
                                      notebook)
            item.name = "notebook%d" % i
            item.author = "revesansparole"

        pjt_workflow.main(session)
        pjt_scene3d.main(session)
