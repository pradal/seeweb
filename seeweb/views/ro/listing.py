from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.auth import Role
from seeweb.ro.search import search


@view_config(route_name='ro_list',
             renderer='templates/ro/listing.jinja2')
def view(request):
    allow_edit = request.unauthenticated_userid is not None

    session = DBSession()

    params = dict(request.params)
    main_search = params.pop('main_search', None)
    if main_search is not None:
        groups = [gr.strip() for gr in main_search.split(" ")
                  if len(gr.strip()) > 0]
        for gr in groups:
            if ":" in gr:
                k, v = gr.split(":")
                params[k.strip()] = v.strip()
            else:
                params["name"] = gr

    res = search(session, params)
    ros = []
    for ro in res:
        role = ro.access_role(session, request.unauthenticated_userid)
        if role != Role.denied:
            ros.append((Role.to_str(role), ro))

    query = " ".join("%s:%s" % kv for kv in params.items())

    return {'allow_edit': allow_edit, 'query': query, 'ros': ros}
