from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.comment import Comment
from seeweb.models.project import Project
from seeweb.model_edit import recompute_project_ratings


@view_config(route_name='comment_edit_score',
             renderer='templates/comment/edit_score.jinja2')
def view(request):
    session = DBSession()
    cid = request.matchdict['cid']
    comment = Comment.get(session, cid)
    if comment is None:
        request.session.flash("Invalid comment", 'warning')
        return HTTPFound(location=request.session['last'])

    # check user credentials
    if request.unauthenticated_userid is None:
        request.session.flash("Action non authorized for anonymous users", 'warning')
        return HTTPFound(location=request.session['last'])

    if 'up' in request.params:
        vote = 'up'
    elif 'down' in request.params:
        vote = 'down'
    else:
        request.session.flash("Invalid vote", 'warning')
        return HTTPFound(location=request.session['last'])

    if 'validate' in request.params:
        if vote == 'up':
            comment.score += 1
        elif vote == 'down':
            comment.score -= 1

        # recompute project ratings
        recompute_project_ratings(session,
                                  Project.get(session, comment.project))

        request.session.flash("Comment voted %s" % vote, 'success')
        return HTTPFound(location=request.session['last'])

    return {"comment": comment,
            "vote": vote,
            "from": request.session['last']}
