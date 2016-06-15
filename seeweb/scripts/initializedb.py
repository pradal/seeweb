from glob import glob
import os
import sys
from PIL import Image
from pyramid.paster import get_appsettings, setup_logging
from pyramid.scripts.common import parse_vars
from sqlalchemy import engine_from_config
from textwrap import dedent
import transaction
from uuid import uuid1

from seeweb.avatar import upload_team_avatar, upload_user_avatar
from seeweb.io import rmtree
from seeweb.models import Base, DBSession
from seeweb.models.auth import Role
from seeweb.models.research_object import ResearchObject
from seeweb.models.ro_article import ROArticle
from seeweb.models.ro_container import ROContainer
from seeweb.models.ro_link import ROLink
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

    # create extra dirs
    for pth in ("data", "data/sessions", "../see_repo"):
        if not os.path.exists(pth):
            os.mkdir(pth)

    # remove sqlite file
    sqlite_pth = "data/seeweb.sqlite"
    if os.path.exists(sqlite_pth):
        os.remove(sqlite_pth)

    # clean data
    for obj_type in ("ro", "team", "user"):
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

        # teams
        subsub_team = Team.create(session, uid="subsubteam")
        subsub_team.description = """Test team only"""
        subsub_team.add_policy(session, doofus0, Role.edit)

        sub_team = Team.create(session, uid="subteam")
        sub_team.description = """Test team only"""
        sub_team.add_policy(session, doofus1, Role.edit)
        sub_team.add_policy(session, subsub_team, Role.edit)

        vplants = Team.create(session, uid="vplants")
        img = Image.open("seeweb/scripts/avatar/vplants.png")
        upload_team_avatar(img, vplants)
        descr = dedent("""
                Team
                ----
                INRIA team based in Montpellier

                """)
        vplants.store_description(descr)
        vplants.add_policy(session, pradal, Role.edit)
        vplants.add_policy(session, fboudon, Role.view)

        oa = Team.create(session, uid="openalea")
        img = Image.open("seeweb/scripts/avatar/openalea.png")
        upload_team_avatar(img, oa)
        descr = dedent("""
                Community
                ---------

                OpenAlea is an open source project primarily aimed at the plant research community.
                It is a distributed collaborative effort to develop Python libraries and tools that address the needs of
                current and future works in Plant Architecture modeling.
                OpenAlea includes modules to analyse, visualize and model the functioning and growth of plant architecture.

                """)
        oa.store_description(descr)
        oa.add_policy(session, revesansparole, Role.edit)
        oa.add_policy(session, pradal, Role.view)
        oa.add_policy(session, sartzet, Role.view)
        oa.add_policy(session, vplants, Role.edit)
        oa.add_policy(session, sub_team, Role.edit)

        # ROs
        ro1 = ResearchObject.create(session,
                                    uuid1().hex,
                                    revesansparole.id,
                                    "RO one")
        ro1.add_policy(session, sartzet, Role.view)
        ro1.add_policy(session, vplants, Role.edit)

        ro2 = ResearchObject.create(session,
                                    uuid1().hex,
                                    revesansparole.id,
                                    "RO two")

        ROLink.connect(session, ro1.id, ro2.id, "contains")

        ro3 = ResearchObject.create(session,
                                    uuid1().hex,
                                    revesansparole.id,
                                    "RO three")

        roc = ROContainer.create(session,
                                 uuid1().hex,
                                 revesansparole.id,
                                 "myproject")
        for i in range(5):
            ro = ResearchObject.create(session,
                                       uuid1().hex,
                                       revesansparole.id,
                                       "RO%d" % i)
            ROLink.connect(session, roc.id, ro.id, "contains")

        roa = ROArticle.create(session,
                                 uuid1().hex,
                                 revesansparole.id,
                                 "test article")
        roa.doi = "10.1016/S0304-3800(98)00100-8"
        ROLink.connect(session, roc.id, roa.id, "contains")
        ROLink.connect(session, ro3.id, roa.id, "use")
