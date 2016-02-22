from pyramid.httpexceptions import HTTPFound

from seeweb.avatar import upload_project_avatar
from seeweb.models.auth import Role
from seeweb.models.content_item import ContentItem
from seeweb.models.project import Project
from seeweb.models.user import User
from seeweb.project.content.explore import explore_sources

from seeweb.project.explore_sources import (fetch_avatar,
                                            fetch_gallery,
                                            fetch_readme)
from seeweb.project.gallery import add_gallery_image, clear_gallery
from seeweb.project.source import has_source
import transaction

tabs = [('Home', 'home'),
        ('Documentation', 'doc'),
        ('Content', 'content'),
        ('Contributors', 'contributors'),
        ('Comments', 'comments')]


def init_min(request, session):
    """Common init for all project views.

    Args:
        request: (Request)
        session: (DBSession)

    Returns:
        (User, dict of (str: any)): user, view_params
    """
    pid = request.matchdict['pid']

    project = Project.get(session, pid)
    if project is None:
        request.session.flash("Project %s does not exists" % pid, 'warning')
        raise HTTPFound(location=request.route_url('home'))

    role = project.access_role(session, request.unauthenticated_userid)
    if role == Role.denied:
        request.session.flash("Access to %s not granted for you" % pid,
                              'warning')
        raise HTTPFound(location=request.route_url('home'))

    view_params = {'project': project}

    return project, role, view_params


def view_init(request, session, tab):
    """Common init for all 'view'.

    Args:
        request: (Request)
        session: (DBSession)
        tab: (str) current tab in view

    Returns:
        (User, dict of (str: any)): user, view_params
    """
    project, role, view_params = init_min(request, session)

    # potential install
    if request.unauthenticated_userid is None:  # TODO can do better
        install_action = None
    else:
        user = User.get(session, request.unauthenticated_userid)
        if user.has_installed(session, project):
            install_action = "uninstall"
        else:
            install_action = "install"

    view_params = {"project": project,
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

    if 'update' in request.params:
        # edit project visibility
        public = 'visibility' in request.params
        project.public = public

    if 'confirm_transfer' in request.params:
        if request.unauthenticated_userid != project.owner:
            request.session.flash("Action non authorized for you", 'warning')
            raise HTTPFound(location=request.route_url('home'))

        user = User.get(session, request.params["new_owner"])
        if user is None:
            msg = "User '%s' is unknown" % request.params["new_owner"]
            request.session.flash(msg, 'warning')
            raise HTTPFound(location=request.current_route_url())

        project.change_owner(session, user)
        loc = request.route_url("project_view_home", pid=project.id)
        transaction.commit()
        raise HTTPFound(location=loc)

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
            request.session.flash("Unable to find suitable readme file",
                                  'warning')

    if 'fetch_gallery' in request.params:
        clear_gallery(project)
        imgs = fetch_gallery(project.id)
        if len(imgs) > 0:
            for img, name in imgs:
                add_gallery_image(project, img, name)

            request.session.flash("gallery submitted", 'success')

    if 'fetch_content' in request.params:
        explore_sources(session, project)

    if "confirm_delete" in request.params:
        if request.unauthenticated_userid != project.owner:
            request.session.flash("Action non authorized for you", 'warning')
            raise HTTPFound(location=request.route_url('home'))

        if Project.remove(session, project):
            transaction.commit()
            request.session.flash("Project '%s' deleted" % project.id,
                                  'success')
        else:
            request.session.flash("Failed to delete '%s'" % project.id,
                                  'warning')
        raise HTTPFound(location=request.route_url('home'))

    return project, view_params


def install_init(request, session):
    """Common actions for install uninstall views

    Args:
        request: (Request)
        session: (DBSession)

    Returns:
        (Project, dict of (str, any)): project, view_params
    """
    project, role, view_params = init_min(request, session)

    if 'cancel' in request.params:
        # back to project page
        loc = request.route_url('project_view_home', pid=project.id)
        raise HTTPFound(location=loc)

    return project, view_params


def content_init(request, session):
    """Common actions for content items views

    Args:
        request: (Request)
        session: (DBSession)

    Returns:
        (Project, ContentItem, dict of (str, any)): project, item, view_params
    """
    project, role, view_params = init_min(request, session)
    cid = request.matchdict['cid']
    item = ContentItem.get(session, cid)
    if item is None:
        # back to project page
        request.session.flash("Object does not exist", 'warning')
        loc = request.route_url('project_view_content', pid=project.id)
        raise HTTPFound(location=loc)

    allow_edition = role == Role.edit

    if allow_edition:
        if "confirm_gallery_addition" in request.params:
            descr = request.params["gallery_item_description"]
            print descr, "add to gallery\n" * 10

    view_params["allow_edition"] = allow_edition
    view_params["cnt_item"] = item
    item_def = item.load_definition()
    view_params["cnt_def"] = item_def

    return project, item, item_def, view_params
