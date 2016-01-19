from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.access import get_comment, get_project
from seeweb.models.edit import recompute_project_ratings
from seeweb.views.tools import get_current_uid


@view_config(route_name='comment_edit_score',
             renderer='templates/comment/edit_score.jinja2')
def view(request):
    session = DBSession()
    cid = request.matchdict['cid']
    comment = get_comment(session, cid)

    if 'up' in request.params:
        vote = 'up'
    elif 'down' in request.params:
        vote = 'down'
    else:
        request.session.flash("Invalid vote", 'warning')
        return HTTPFound(location=request.session['last'])

    # check user credentials
    if get_current_uid(request) is None:
        request.session.flash("Action non authorized for anonymous users", 'warning')
        return HTTPFound(location=request.session['last'])

    if 'validate' in request.params:
        if vote == 'up':
            comment.score += 1
        elif vote == 'down':
            comment.score -= 1

        # recompute project ratings
        recompute_project_ratings(session, get_project(session, comment.project))

        request.session.flash("Comment voted %s" % vote, 'success')
        return HTTPFound(location=request.session['last'])

    return {"comment": comment,
            "vote": vote,
            "from": request.session['last']}
