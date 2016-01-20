from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.comment import Comment


@view_config(route_name='admin_comments',
             renderer='templates/admin/comments.jinja2',
             permission='admin')
def view(request):
    session = DBSession()
    query = session.query(Comment)
    if 'query' in request.params and "all" not in request.params:
        search_pattern = "%s%%" % request.params['query']
        query = query.filter(Comment.author.like(search_pattern))
    else:
        search_pattern = ""

    return {'comments': query.all(),
            'search_pattern': search_pattern}
