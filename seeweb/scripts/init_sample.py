from textwrap import dedent

from seeweb.models.auth import Role
from seeweb.models.research_object import ResearchObject
from seeweb.models.ro_link import ROLink

from seeweb.ro.article.models.ro_article import ROArticle
from seeweb.ro.container.models.ro_container import ROContainer

from init_users import users, teams


def main(session):
    ro1 = ResearchObject()
    ro1.init(session, dict(owner=users[0].id, name="RO one"))

    ro1.add_policy(session, users[0], Role.view)
    ro1.add_policy(session, teams[2], Role.edit)

    ro2 = ResearchObject()
    ro2.init(session, dict(owner=users[0].id, name="RO two"))

    ROLink.connect(session, ro1.id, ro2.id, "contains")

    ro3 = ResearchObject()
    ro3.init(session, dict(owner=users[0].id, name="RO three"))

    ros = []
    for i in range(5):
        ro = ResearchObject()
        ro.init(session, dict(owner=users[0].id, name="RO%d" % i))
        ros.append(ro)

    roc = ROContainer()
    roc.init(session, dict(owner=users[0].id,
                           name="myproject",
                           remote="https://github.com/revesansparole/roc",
                           contents=ros))

    ros = []
    for i in range(5):
        ro = ResearchObject()
        ro.init(session, dict(owner=users[1].id, name="ROcp%d" % i))
        ros.append(ro)

    ro = ROArticle()
    ro.init(session, dict(owner=users[2].id, name="cp article"))
    ro.add_policy(session, users[0], Role.view)
    ros.append(ro)

    roc2 = ROContainer()
    roc2.init(session, dict(owner=users[2].id,
                            name="CPproject",
                            contents=ros))

    roa = ROArticle()
    roa.init(session, dict(owner=users[0].id, name="test article"))
    roa.doi = "10.1016/S0304-3800(98)00100-8"
    descr = dedent("""
        We present a new approach to simulate the distribution of natural
        light within plant canopies. The canopy is described in 3D, each
        organ being represented by a set of polygons. Our model calculates
        the light incident on each polygon. The principle is to distinguish
        for each polygon the contribution of the light coming directly from
        light sources, the light scattered from close polygons and that
        scattered from far polygons. Close polygons are defined as located
        inside a sphere surrounding the studied polygon and having a
        diameter Ds. The direct light is computed by projection. The
        exchanges between close polygons are computed by the radiosity
        method, whereas the contribution from far polygons is estimated by
        a multi-layer model. The main part of computing time corresponds to
        the calculations of the geometric coefficients of the radiosity
        system. Then radiative exchanges can be quickly simulated for
        various conditions of the angular distribution of incoming light
        and various optical properties of soil and phytolelements.
        Simulations compare satisfactorily with those produced by a Monte
        Carlo ray tracing. They show that considering explicitly the close
        neighboring of each polygon improves the estimation of organs
        irradiance, by taking into account the local variability of fluxes.
        For a virtual maize canopy, these estimations are satisfying with
        Ds=0.5 m; in these conditions, the simulation time on a workstation
        was 25 min for a canopy of 100 plants.""")
    roa.store_description(descr)
    ROLink.connect(session, roc.id, roa.id, "contains")
    ROLink.connect(session, ro3.id, roa.id, "use")
