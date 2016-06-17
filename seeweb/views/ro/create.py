from datetime import datetime
from dateutil.parser import parse
from json import load
from os.path import join as pj
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from uuid import uuid1

from seeweb.models import DBSession
from seeweb.models.research_object import ResearchObject
from seeweb.ro.article.models.ro_article import ROArticle


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
            pth = "../see_repo"
            with open(pj(pth, file_name), 'wb') as f:
                f.write(input_file.read())

            with open(pj(pth, file_name), 'r') as f:
                data = load(f)

                data["creation"] = parse(data["creation"])
                uid = uuid1().hex#data["id"]
                session = DBSession()
                ro_type = data.get("type", 'ro')
                if ro_type == 'article':
                    ro = ROArticle.create(session, uid, data["creator"], data["title"])
                else:
                    ro = ResearchObject.create(session, uid, data["creator"], data["title"])
                if ro is not None:
                    ro.store_description(data['description'])
                    return HTTPFound(location=request.route_url("ro_view_home", uid=uid))



    uid = uuid1().hex
    creator = request.unauthenticated_userid  # TODO test first
    created = datetime.now()
    version = 0

    ro_types = ["plain", "container", "article"]

    return dict(uid=uid, creator=creator, created=created, version=version, ro_types=ro_types)
