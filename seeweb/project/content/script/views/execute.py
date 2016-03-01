from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from StringIO import StringIO
import sys
import traceback

from seeweb.models import DBSession
from seeweb.models.user import User
from seeweb.views.project.commons import content_init


@view_config(route_name='project_content_script_execute',
             renderer='json')
def view(request):
    session = DBSession()
    project, script, script_def, view_params = content_init(request, session)

    user = User.get(session, request.unauthenticated_userid)
    if user is None:
        request.session.flash("action not granted to you", 'warning')
        raise HTTPFound(location=request.route_url('home'))
    elif project.id not in (inst.project for inst in user.installed):
        msg = "action not granted to you, need to install package first"
        request.session.flash(msg, 'warning')
        loc = request.route_url('user_view_home', uid=user.id)
        raise HTTPFound(location=loc)

    stream = StringIO()
    mem = sys.stdout
    sys.stdout = stream
    code = compile(script_def['source'], script.name, 'exec')
    res = dict(stdout="", stderr="")
    try:
        eval(code)
    except Exception as e:
        traceback.print_exc(file=stream)
        res['stderr'] = stream.getvalue()

    sys.stdout = mem

    res['stdout'] = stream.getvalue()

    return res
