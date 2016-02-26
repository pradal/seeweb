from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.content_item import ContentItem


@view_config(route_name='project_content')
def view(request):
    """REST API to access a project content from its id only

    Args:
        request: (Request)

    Returns:
        json file if schema required
        or http indirection to resource
    """
    session = DBSession()

    cid = request.matchdict['cid']
    item = ContentItem.get(session, cid)
    if item is None:
        request.session.flash("Content %s does not exists" % cid, 'warning')
        raise HTTPFound(location=request.route_url('home'))
    else:
        loc = request.route_url('project_content_%s_view_item' % item.category,
                                pid=item.project,
                                cid=item.id)
        return HTTPFound(location=loc)
