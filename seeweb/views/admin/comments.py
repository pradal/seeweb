from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.comment import Comment


@view_config(route_name='admin_comments',
             renderer='templates/admin/comments.jinja2',
             permission='admin')
def view(request):
    session = DBSession()
    query = session.query(Comment)

    search_pattern = request.params.get("main_search", "")
    if search_pattern != "":
        query = query.filter(Comment.project.like("%s%%" % search_pattern))

    return {'comments': query.all(),
            'search_pattern': search_pattern}
