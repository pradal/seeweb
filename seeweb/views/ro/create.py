from datetime import datetime
from dateutil.parser import parse
from os.path import dirname
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from uuid import uuid1

from seeweb.io import rmtree, upload_file
from seeweb.models import DBSession
from seeweb.ro.explore import create_from_file, register


@view_config(route_name='ro_create',
             renderer='templates/ro/create.jinja2')
def view(request):
    if request.unauthenticated_userid is None:
        msg = "Operation non authorized for anonymous users"
        request.session.flash(msg, 'warning')
        return HTTPFound(location=request.route_url("home"))

    if "new_ro" in request.params:
        session = DBSession()
        uid = request.params["ro_id"]
        created = parse(request.params["created"])
        name = request.params["name"]
        ro_type = request.params["ro_type"]

        # do some checking
        assert len(uid) == 32

        print uid, created, name, ro_type, "\n" * 10

        # gather data
        data = dict(id=uid,
                    owner=request.unauthenticated_userid,
                    created=created,
                    name=name,
                    version=0)

        # create RO
        ro = register(session, ro_type, data)
        return HTTPFound(location=request.route_url("ro_view_home", uid=ro.id))
    elif "submit_upload" in request.params:
        field_storage = request.params["upload_file"]
        if field_storage == "":
            msg = "Need to select file first"
            request.session.flash(msg, 'warning')
        else:
            pth = upload_file(field_storage)
            session = DBSession()
            ro = create_from_file(session, pth, request.unauthenticated_userid)
            rmtree(dirname(pth))

            if ro is None:
                msg = "Unable to find a valid RO in this file"
                request.session.flash(msg, 'warning')
            else:
                return HTTPFound(location=request.route_url("ro_view_home", uid=ro.id))

    uid = uuid1().hex
    created = datetime.now()

    ro_types = ["plain", "container", "article"]

    return dict(uid=uid, created=created, ro_types=ro_types)
