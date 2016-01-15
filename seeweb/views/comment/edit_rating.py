from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from seeweb.views.tools import get_current_uid

from .tools import get_comment


@view_config(route_name='comment_edit_rating',
             renderer='templates/comment/edit_rating.jinja2')
def view(request):
    cid = request.matchdict['cid']
    vote = request.matchdict['vote']
    comment = get_comment(cid)

    current_uid = get_current_uid(request)

    if vote == 'up':
        comment.rating += 1
    elif vote == 'down':
        comment.rating -= 1
    else:
        request.session.flash("Invalid vote", 'warning')

    return {"comment": comment,
            "vote": vote,
            "from": request.session['last']}
