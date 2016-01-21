from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.access import get_project
from seeweb.models.edit import create_comment, recompute_project_ratings


def validate_comment(request, session, author, pid, txt, ratings):
    # check user credentials
    current_uid = request.unauthenticated_userid
    if current_uid != author:
        request.session.flash("Action non authorized", 'warning')
        raise HTTPFound(location=request.session['last'])

    project = get_project(session, pid)
    if project is None:
        request.session.flash("Comment associated to bad project", 'warning')
        raise HTTPFound(location=request.session['last'])

    if len(txt) == 0:
        request.session.flash("Some text maybe??", 'warning')
        return False

    # register new comment
    create_comment(session, pid, author, txt, ratings)

    # recompute project ratings
    recompute_project_ratings(session, project)

    return True


@view_config(route_name='comment_edit_new',
             renderer='templates/comment/edit_new.jinja2')
def view(request):
    session = DBSession()

    author = request.params.get("author", "unknown")
    pid = request.params.get("project", "unknown")
    txt = request.params.get("text")

    rating_names = ["Value", "Documentation", "Installation", "Usage"]
    ratings = [(name, float(request.params.get("rating_%s" % name.lower(), 2.5))) for name in rating_names]

    if 'validate' in request.params:
        if validate_comment(request, session, author, pid, txt, ratings):
            return HTTPFound(location=request.session['last'])

    return {"from": request.session['last'],
            "author": author,
            "pid": pid,
            "txt": txt,
            "ratings": ratings}