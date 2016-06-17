from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.research_object import ResearchObject
from seeweb.models.ro_link import ROLink

from .commons import edit_init


def add_link(request, session, ro):
    """Add a new 'use' link between this RO and another

    Args:
        request (Request):
        session (DBSession):
        ro (ResearchObject):

    Returns:
        (None|uid): None if something failed, created link
    """
    uid = request.params.get('ro_id', "")
    if len(uid) == 0:
        request.session.flash("Enter a RO id first", 'warning')
        return None

    # check whether the RO is already associated to this RO
    if uid == ro.id:
        request.session.flash("Can not create link with oneself", 'warning')
        return None

    linked = [link.target for link in ro.out_links if link.type == 'use']
    if uid in linked:
        request.session.flash("%s is already linked" % uid, 'warning')
        return None

    # check whether uid correspond to a valid RO
    tgt = ResearchObject.get(session, uid)
    if tgt is None:
        request.session.flash("%s is not a valid RO" % uid, 'warning')
        return None

    # create link
    link = ROLink.connect(session, ro.id, uid, "use")
    return link


@view_config(route_name='ro_edit_links',
             renderer='templates/ro/edit_links.jinja2')
def view(request):
    session = DBSession()
    ro, view_params = edit_init(request, session, 'links')

    if "new_link" in request.params or request.params.get("ro_id", "") != "":
        if add_link(request, session, ro) is not None:
            loc = request.current_route_url()
            return HTTPFound(location=loc)

    # check for link removal
    for link in ro.out_links + ro.in_links:
        if "rm_%s" % link.id in request.params:
            ROLink.remove(session, link)
            request.session.flash("Link removed", 'success')

            loc = request.current_route_url()
            return HTTPFound(location=loc)

    links = []
    for link in ro.out_links:
        links.append((link.id, "self", link.type, link.target))
    for link in ro.in_links:
        links.append((link.id, link.source, link.type, "self"))

    view_params["links"] = links

    return view_params
