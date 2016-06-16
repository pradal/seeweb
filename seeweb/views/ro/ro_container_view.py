from jinja2 import Markup
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.auth import Role
from seeweb.models.research_object import ResearchObject
from seeweb.models.ro_link import ROLink

from seeweb.views.ro.commons import view_init_min


def append_ro(request, session, container):
    """Add a new RO in this container.

    Args:
        request (Request):
        session (DBSession):
        container (ROContainer):

    Returns:
        (None|uid): None if something failed, created link
    """
    uid = request.params.get('ro_id', "")
    if len(uid) == 0:
        request.session.flash("Enter a RO id first", 'warning')
        return None

    # check whether the RO is already a member of the container
    content = [link.target for link in container.out_links if link.type == 'contains']
    if uid in content:
        request.session.flash("%s is already in this container" % uid, 'warning')
        return None

    # check whether uid correspond to a valid RO
    ro = ResearchObject.get(session, uid)
    if ro is None:
        request.session.flash("%s is not a valid RO" % uid, 'warning')
        return None

    # check whether user has 'install' rights on this RO
    role = ro.access_role(session, request.unauthenticated_userid)
    if role < Role.install:
        request.session.flash("You're not allowed to add %s to this container" % uid, 'warning')
        return None

    # create link
    link = ROLink.connect(session, container.id, uid, "contains")
    return link


@view_config(route_name='ro_container_view',
             renderer='templates/ro/container_view.jinja2')
def view(request):
    session = DBSession()
    ro, view_params = view_init_min(request, session)

    if 'new_content' in request.params and view_params["allow_edit"]:
        if append_ro(request, session, ro) is not None:
            loc = request.current_route_url()
            return HTTPFound(location=loc)

    view_params['description'] = Markup(ro.html_description())

    content = [link.target for link in ro.out_links if link.type == "contains"]
    view_params['content'] = content

    return view_params
