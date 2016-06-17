from datetime import datetime
from os.path import dirname
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from uuid import uuid1

from seeweb.io import rmtree, upload_file
from seeweb.models import DBSession
from seeweb.models.research_object import ResearchObject
from seeweb.ro.explore import create_from_file


@view_config(route_name='ro_create',
             renderer='templates/ro/create.jinja2')
def view(request):
    if "new_ro" in request.params:
        session = DBSession()
        uid = request.params["ro_id"]
        creator = request.params["creator"]
        created = request.params["created"]
        version = request.params["version"]
        title = request.params["title"]
        ro_type = request.params["ro_type"]

        # do some checking
        print uid, creator, title, ro_type

        # create RO
        if ResearchObject.create(session, uid, creator, title):
            return HTTPFound(location=request.route_url("ro_view_home", uid=uid))
    elif "submit_upload" in request.params:
        field_storage = request.params["upload_file"]
        if field_storage == "":
            msg = "Need to select file first"
            request.session.flash(msg, 'warning')
        else:
            pth = upload_file(field_storage)
            session = DBSession()
            ro = create_from_file(session, pth, request.unauthenticated_userid)
            # rmtree(dirname(pth))

            if ro is None:
                msg = "Unable to find a valid RO in this file"
                request.session.flash(msg, 'warning')
            else:
                return HTTPFound(location=request.route_url("ro_view_home", uid=ro.id))

    uid = uuid1().hex
    creator = request.unauthenticated_userid  # TODO test first
    created = datetime.now()
    version = 0

    ro_types = ["plain", "container", "article"]

    return dict(uid=uid, creator=creator, created=created, version=version, ro_types=ro_types)
