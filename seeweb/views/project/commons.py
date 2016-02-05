from pyramid.httpexceptions import HTTPFound

from seeweb.avatar import upload_project_avatar
from seeweb.model_access import get_project, get_user, project_access_role
from seeweb.model_edit import remove_project
from seeweb.models.auth import Role
from seeweb.project.explore_sources import (fetch_avatar,
                                            fetch_gallery,
                                            fetch_readme)
from seeweb.project.gallery import add_gallery_image
from seeweb.project.source import has_source
import transaction

tabs = [('Home', 'home'),
        ('Documentation', 'doc'),
        ('Source', 'source'),
        ('Contributors', 'contributors'),
        ('Comments', 'comments')]


def view_init(request, session, tab):
    """Common init for all 'view'.

    Args:
        request: (Request)
        session: (DBSession)
        tab: (str) current tab in view

    Returns:
        (User, dict of (str: any)): user, view_params
    """
    pid = request.matchdict['pid']

    project = get_project(session, pid)
    if project is None:
        request.session.flash("Project %s does not exists" % pid, 'warning')
        raise HTTPFound(location=request.route_url('home'))

    current_uid = request.unauthenticated_userid
    role = project_access_role(session, project, current_uid)
    if role == Role.denied:
        request.session.flash("Access to %s not granted for you" % pid,
                              'warning')
        raise HTTPFound(location=request.route_url('home'))

    # potential install
    if current_uid is None:  # TODO can do better
        install_action = None
    else:
        user = get_user(session, current_uid)
        if project in user.installed:
            install_action = "uninstall"
        else:
            install_action = "install"

    view_params = {"current_uid": current_uid,
                   "project": project,
                   "tabs": tabs,
                   "tab": tab,
                   "allow_edit": (role == Role.edit),
                   "install_action": install_action,
                   "sections": [],
                   "ratings": project.format_ratings(),
                   "has_source": has_source(project.id)}

    return project, view_params


def edit_init(request, session, tab):
    """Common init for all 'edit' views.

    Args:
        request: (request)
        session: (DBSession)
        tab: (str) currently edited tab

    Returns:
        (User, dict of (str: any)): user, view_params
    """
    project, view_params = view_init(request, session, tab)

    if not view_params["allow_edit"]:
        msg = "Access to %s edition not granted for you" % project.id
        request.session.flash(msg, 'warning')
        raise HTTPFound(location=request.route_url('home'))

    if 'back' in request.params:
        # request.session.flash("Edition stopped", 'success')
        loc = request.route_url('project_view_%s' % tab, pid=project.id)
        raise HTTPFound(location=loc)

    if 'delete' in request.params:
        request.session.flash("Edition stopped", 'success')
        loc = request.route_url('home')
        raise HTTPFound(location=loc)

    if 'update' in request.params:
        # edit project visibility
        public = 'visibility' in request.params
        project.public = public

    if 'fetch_avatar' in request.params:
        try:
            img = fetch_avatar(project.id)
            if img is None:
                request.session.flash("No avatar found in sources", 'warning')
            else:
                upload_project_avatar(img, project)
                request.session.flash("Avatar submitted", 'success')
        except IOError:
            request.session.flash("Unable to read image", 'warning')

    if 'fetch_readme' in request.params:
        try:
            txt = fetch_readme(project.id)
            project.store_description(txt)
            request.session.flash("Readme submitted", 'success')
        except IOError:
            request.session.flash("Unable to find suitable readme file", 'warning')

    if 'fetch_dependencies' in request.params:
        request.session.flash("TODO dependencies submitted", 'success')

    if 'fetch_gallery' in request.params:
        imgs = fetch_gallery(project.id)
        if len(imgs) > 0:
            for img, name in imgs:
                add_gallery_image(project, img, name)

            request.session.flash("TODO gallery submitted", 'success')

    if "confirm_delete" in request.params:
        if remove_project(session, project):
            transaction.commit()
            request.session.flash("Project '%s' deleted" % project.id, 'success')
        else:
            request.session.flash("Failed to delete '%s'" % project.id, 'warning')
        raise HTTPFound(location=request.route_url('home'))

    return project, view_params
