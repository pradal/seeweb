from dateutil.parser import parse
import json
from os import remove
from os.path import join as pj
from os.path import basename, dirname, splitext
from uuid import uuid1
from zipfile import BadZipfile, ZipFile

from seeweb.avatar import upload_ro_avatar
from seeweb.io import find_files
from seeweb.models.research_object import ResearchObject
from seeweb.models.ro_link import ROLink
from seeweb.ro.article.models.ro_article import ROArticle
from seeweb.ro.container.models.ro_container import ROContainer
from seeweb.ro.explore_sources import fetch_avatar, fetch_readme
from seeweb.ro.interface.models.ro_interface import ROInterface
from seeweb.ro.workflow.models.ro_workflow import ROWorkflow
from seeweb.ro.workflow_node.models.ro_workflow_node import ROWorkflowNode
from seeweb.ro.workflow_prov.models.ro_workflow_prov import ROWorkflowProv
from seeweb.rodata.image.models.ro_image import ROImage
from seeweb.rodata.scene3d.models.ro_scene3d import ROScene3d


ro_factory = dict(ro=ResearchObject,
                  article=ROArticle,
                  container=ROContainer,
                  image=ROImage,
                  interface=ROInterface,
                  scene3d=ROScene3d,
                  workflow=ROWorkflow,
                  workflow_node=ROWorkflowNode,
                  workflow_prov=ROWorkflowProv)


def validate(pth):
    """Check the content of a file to decide the type of RO it contains.

    Args:
        pth (str):

    Returns:
        (str): RO type or None if no RO correspond
    """
    try:
        with open(pth, 'r') as f:
            ro_def = json.load(f)
            for kwd in ('id', 'created', 'owner', 'name', 'description'):
                if kwd not in ro_def:
                    print "missing", kwd
                    return None

            ro_type = ro_def.get("type", 'ro')
            return ro_type
    except ValueError:
        return None


def register(session, ro_type, ro_def):
    """

    Args:
        session (DBSession):
        ro_type (str): type of RO to register
        ro_def (dict): json def of RO

    Returns:
        (ResearchObject): or one of its subclass
    """
    if ro_type not in ro_factory:
        raise UserWarning("unrecognized RO type '%s'" % ro_type)

    ro = ro_factory[ro_type]()
    ro.init(session, ro_def)

    return ro


def create(session, pth, ro_type):
    """Create a RO from content of file in pth

    Args:
        session (DBSession):
        pth (str): path to resource
        ro_type (str): type of RO to create

    Returns:
        (ResearchObject): or one of its subclass
    """
    with open(pth, 'r') as f:
        data = json.load(f)
        data["created"] = parse(data["created"])

    return register(session, ro_type, data)


def create_from_file(session, pth, user):
    """Create a RO from a a file.

    Notes: if pth is a zipfile, it will be extracted and
           a ROContainer will be created with he content

    Args:
        session (DBSession):
        pth (str): path to file to read
        user (str): id of user

    Returns:
        (ResearchObject): or None if nothing has been recognized in
                          the file
    """
    # try to unpack zip files
    try:
        with ZipFile(pth, 'r') as myzip:
            myzip.extractall(pj(dirname(pth), "archive"))

        remove(pth)
        # explore directory
        ros = []
        for fpth, fname in find_files(pj(dirname(pth), "archive"), ["*.wkf"]):
            ro_type = validate(fpth)
            if ro_type is not None:
                ros.append(create(session, fpth, ro_type))

        if len(ros) == 0:
            return None
        else:
            name = splitext(basename(pth))[0]
            cont = ROContainer()
            cont.init(session, dict(id=uuid1().hex,
                                    owner=user,
                                    name=name))
            for ro in ros:
                ROLink.connect(session, cont.id, ro.id, "contains")

            # search for project avatar
            avatar = fetch_avatar(pj(dirname(pth), "archive"))
            if avatar is not None:
                upload_ro_avatar(avatar, cont)

            # search project description in README
            descr = fetch_readme(pj(dirname(pth), "archive"))
            cont.store_description(descr)

            return cont
    except BadZipfile:
        # not a zip file, try to import single file
        ro_type = validate(pth)
        if ro_type is None:
            return None
        else:
            ro = create(session, pth, ro_type)
            return ro
