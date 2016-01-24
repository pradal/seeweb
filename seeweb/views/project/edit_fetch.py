from io import BytesIO
from PIL import Image
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from urlparse import urlsplit

from seeweb.models import DBSession
from seeweb.models.access import get_project, project_access_role
from seeweb.models.auth import Role
from seeweb.tools import github, local_provider
from seeweb.views.tools import add_gallery_image, clear_gallery, upload_avatar


@view_config(route_name='project_edit_fetch',
             renderer='templates/project/edit_fetch.jinja2')
def view(request):
    session = DBSession()
    pid = request.matchdict['pid']

    if 'cancel' in request.params:
        loc = request.route_url('project_edit_source', pid=pid)
        raise HTTPFound(location=loc)

    project = get_project(session, pid)
    if project is None:
        request.session.flash("Project %s does not exists" % pid, 'warning')
        raise HTTPFound(location=request.route_url('home'))

    current_uid = request.unauthenticated_userid
    role = project_access_role(session, project, current_uid)
    if role != Role.edit:
        request.session.flash("Access to %s not granted for you" % pid,
                              'warning')
        raise HTTPFound(location=request.route_url('home'))

    if project.src_url == "":
        request.session.flash("Need some source url, update project first?",
                              'warning')
        loc = request.route_url('project_edit_source', pid=project.id)
        raise HTTPFound(location=loc)

    # find relevant provider
    url = urlsplit(project.src_url)
    if url.netloc == "":  # local used for debug purpose
        provider = "local"
    elif url.netloc == "github.com":
        provider = "github"
    else:
        request.session.flash("Provider '%s' not recognized" % url.netloc,
                              'warning')
        loc = request.route_url('project_edit_source', pid=project.id)
        raise HTTPFound(location=loc)

    view_params = {"project": project,
                   "provider": provider}

    for name in ["source",
                 "readme",
                 "avatar",
                 "doc",
                 "contributors",
                 "dependencies",
                 "gallery"]:
        view_params[name] = name in request.params

    # fetch information
    if "validate" in request.params:
        if provider == 'local':
            fetch_success = True
            pth = url.path

            if 'readme' in request.params:
                try:
                    readme = local_provider.fetch_readme(pth)
                    project.description = readme
                except IOError:
                    msg = "Unable to fetch README from local dir"
                    request.session.flash(msg, 'warning')
                    fetch_success = False

            if 'avatar' in request.params:
                try:
                    avatar = local_provider.fetch_avatar(pth)
                    img = Image.open(BytesIO(avatar))
                    upload_avatar(img, project, 'project')
                except IOError:
                    msg = "Unable to fetch avatar from local dir"
                    request.session.flash(msg, 'warning')
                    fetch_success = False

            if 'gallery' in request.params:
                clear_gallery(project.id)
                for img_name, img in local_provider.fetch_gallery_images(pth):
                    add_gallery_image(project.id, img, img_name)

            if fetch_success:
                loc = request.route_url('project_edit_source', pid=project.id)
                return HTTPFound(location=loc)

        elif provider == 'github':
            fetch_success = True
            user = request.params["login"]
            pwd = request.params["password"]

            try:
                gh, repo = github.ensure_login(user, pwd, project.owner, project.id)  # bug find real owner, project id in github url
            except UserWarning:
                request.session.flash("Unable to connect to %s" % provider,
                                      'warning')
                return view_params

            if 'readme' in request.params:
                try:
                    readme = github.fetch_readme(repo)
                    project.description = readme
                except IOError:
                    msg = "Unable to fetch README from github"
                    request.session.flash(msg, 'warning')
                    fetch_success = False

            if 'avatar' in request.params:
                try:
                    avatar = github.fetch_avatar(repo)
                    img = Image.open(BytesIO(avatar))
                    upload_avatar(img, project, 'project')
                except IOError:
                    msg = "Unable to fetch avatar from github"
                    request.session.flash(msg, 'warning')
                    fetch_success = False

            if fetch_success:
                loc = request.route_url('project_edit_source', pid=project.id)
                return HTTPFound(location=loc)

        else:
            request.session.flash("Provider '%s' not recognized" % url.netloc,
                                  'warning')
            loc = request.route_url('project_edit_source', pid=project.id)
            raise HTTPFound(location=loc)

    return view_params
