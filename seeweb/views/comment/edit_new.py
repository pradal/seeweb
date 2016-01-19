from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.access import get_comment
# from seeweb.views.tools import get_current_uid


@view_config(route_name='comment_edit_new',
             renderer='templates/comment/edit_new.jinja2')
def view(request):
    session = DBSession()

    author = request.params.get("author", "unknown")
    pid = request.params.get("project", "unknown")
    txt = request.params.get("text")

    # check user credentials
    # current_uid = get_current_uid(request)

    return {"from": request.session['last'],
            "author": author,
            "pid": pid,
            "txt": txt}
