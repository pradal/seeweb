from glob import glob
from importlib import import_module
import os
from os.path import basename, dirname, splitext
import sys
from pyramid.paster import get_appsettings, setup_logging
from pyramid.scripts.common import parse_vars
from sqlalchemy import engine_from_config
import transaction

from seeweb.io import rmtree
from seeweb.models import Base, DBSession

import pjt_auth_managment
import pjt_data
import pjt_workflow
import init_sample
from init_sample import containers
import init_users
from init_users import users

for dname in glob("seeweb/ro/*/"):
    dname = dname.replace("\\", "/")
    ro_type = basename(dirname(dname))
    for module_pth in glob(dname + "models/*.py"):
        module_name = splitext(basename(module_pth))[0]
        if module_name != "__init__":
            import_module('seeweb.ro.%s.models.%s' % (ro_type, module_name))


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

        init_users.main(session)
        init_sample.main(session)

        pjt_auth_managment.main(session, users[0], containers[0])
        pjt_data.main(session, users[0], containers[0])
        pjt_workflow.main(session, users[0], containers[0])
