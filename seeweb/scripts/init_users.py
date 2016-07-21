from PIL import Image
from textwrap import dedent

from seeweb.avatar import upload_team_avatar, upload_user_avatar
from seeweb.models.auth import Role
from seeweb.models.team import Team
from seeweb.models.user import User

users = []
teams = []


def main(session):
    # users
    revesansparole = User.create(session,
                                 uid='revesansparole',
                                 name="Jerome Chopard",
                                 email="revesansparole@gmail.com")

    img = Image.open("seeweb/scripts/avatar/revesansparole.png")
    upload_user_avatar(img, revesansparole)
    users.append(revesansparole)

    doofus0 = User.create(session,
                          uid='doofus%d' % 0,
                          name="Dummy Doofus",
                          email="dummy.doofus@email.com")
    users.append(doofus0)

    doofus1 = User.create(session,
                          uid='doofus%d' % 1,
                          name="Dummy Doofus",
                          email="dummy.doofus@email.com")
    users.append(doofus1)

    pradal = User.create(session,
                         uid='pradal',
                         name="Christophe Pradal",
                         email="christophe.pradal@inria.fr")
    img = Image.open("seeweb/scripts/avatar/pradal.png")
    upload_user_avatar(img, pradal)
    users.append(pradal)

    sartzet = User.create(session,
                          uid='sartzet',
                          name="Simon Artzet",
                          email="simon.aertzet@inria.fr")
    img = Image.open("seeweb/scripts/avatar/sartzet.png")
    upload_user_avatar(img, sartzet)
    users.append(sartzet)

    fboudon = User.create(session,
                          uid='fboudon',
                          name="Fred Boudon",
                          email="fred.boudon@inria.fr")
    img = Image.open("seeweb/scripts/avatar/fboudon.png")
    upload_user_avatar(img, fboudon)
    users.append(fboudon)

    # teams
    subsub_team = Team.create(session, uid="subsubteam")
    subsub_team.description = """Test team only"""
    subsub_team.add_policy(session, doofus0, Role.edit)
    teams.append(subsub_team)

    sub_team = Team.create(session, uid="subteam")
    sub_team.description = """Test team only"""
    sub_team.add_policy(session, doofus1, Role.edit)
    sub_team.add_policy(session, subsub_team, Role.edit)
    teams.append(sub_team)

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
    teams.append(vplants)

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
    teams.append(oa)
