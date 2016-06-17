from datetime import datetime
from os import remove
from os.path import join as pj
from os.path import splitext
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from uuid import uuid1
from zipfile import BadZipfile, ZipFile

from seeweb.io import find_files, rmtree
from seeweb.models import DBSession
from seeweb.models.research_object import ResearchObject
from seeweb.models.ro_link import ROLink
from seeweb.ro.explore import create, validate
from seeweb.ro.container.models.ro_container import ROContainer


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
        print "file\n" * 10
        field_storage = request.params["upload_file"]
        if field_storage == "":
            msg = "Need to select file first"
            request.session.flash(msg, 'warning')
        else:
            file_name = str(field_storage.filename)
            input_file = field_storage.file
            input_file.seek(0)
            pth = pj("../see_repo", file_name)
            with open(pth, 'wb') as f:
                f.write(input_file.read())

            # try to unpack zip files
            try:
                with ZipFile(pth, 'r') as myzip:
                    myzip.extractall(pj("../see_repo", "archive"))

                remove(pth)
                # explore directory
                ros = []
                for pth, fname in find_files(pj("../see_repo", "archive"), ["*.wkf"]):
                    ro_type = validate(pth)
                    if ro_type is not None:
                        session = DBSession()
                        ros.append(create(session, pth, ro_type))

                rmtree(pj("../see_repo", "archive"))

                if len(ros) == 0:
                    msg = "Unable to find a valid RO in this file"
                    request.session.flash(msg, 'warning')
                else:
                    cid = uuid1().hex
                    cont = ROContainer.create(session, cid, request.unauthenticated_userid, splitext(file_name)[0])
                    for ro in ros:
                        ROLink.connect(session, cont.id, ro.id, "contains")

                    return HTTPFound(location=request.route_url("ro_view_home", uid=cont.id))
            except BadZipfile:
                # not a zip file, try to import single file
                ro_type = validate(pth)
                if ro_type is None:
                    msg = "Unable to find a valid RO in this file"
                    request.session.flash(msg, 'warning')
                else:
                    session = DBSession()
                    ro = create(session, pth, ro_type)
                    return HTTPFound(location=request.route_url("ro_view_home", uid=ro.id))


    uid = uuid1().hex
    creator = request.unauthenticated_userid  # TODO test first
    created = datetime.now()
    version = 0

    ro_types = ["plain", "container", "article"]

    return dict(uid=uid, creator=creator, created=created, version=version, ro_types=ro_types)
