from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.project import Project
# from seeweb.models.project_content.content import Content, item_types
from seeweb.project.source import parse_hostname

from .commons import view_init


@view_config(route_name='project_view_content',
             renderer='templates/project/view_content.jinja2')
def view(request):
    session = DBSession()
    project, view_params = view_init(request, session, 'content')

    if len(project.src_url) > 0:
        hostname = parse_hostname(project.src_url)
    else:
        hostname = ""

    view_params["hostname"] = hostname

    # dependencies
    dependencies = []
    for dep in project.dependencies:
        pjt = Project.get(session, dep.name)
        if pjt is None:
            dependencies.append((dep.name, "ver: %s" % dep.version, False))
        else:
            dependencies.append((pjt, "ver: %s" % dep.version, True))

    view_params["dependencies"] = dependencies

    # explore sources
    cnt = project.fetch_content(session)
    view_params["content"] = cnt
    view_params["sections"] = ["dependencies"] + cnt.keys()

    return view_params
