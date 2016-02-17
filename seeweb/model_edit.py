"""Set of functions used to edit objects in models
"""
from uuid import uuid1

from models.project_content.content import Content, item_types
from models.project_content.executable import Executable
from models.project_content.interface import Interface
from models.project_content.notebook import Notebook
from models.project_content.workflow_node import WorkflowNode
from models.project_content.workflow import Workflow


def add_content(session, project):
    """Add project content to a project.

    Args:
        session: (DBSession)
        project: (Project)

    Returns:
        (Content)
    """
    cnt = Content(id=project.id)
    session.add(cnt)

    return cnt


def _ensure_project_content(session, project):
    """Ensure project has a project content.

    Args:
        session: (DBSession)
        project: (Project)

    Returns:
        (ProjectContent)
    """
    cnt = Content.get(session, project.id)
    if cnt is None:
        cnt = add_content(session, project)

    return cnt


def create_executable(session, project, name):
    """Create a new executable description and associate it to a project.

    Args:
        session: (DBSession)
        project: (Project) an already existing project
        name: (str) name of the executable

    Returns:
        (Executable)
    """
    cnt = _ensure_project_content(session, project)

    executable = Executable(id=uuid1().hex, cnt=cnt.id, name=name)
    session.add(executable)

    return executable


def create_interface(session, project, name):
    """Create a new interface description and associate it to a project.

    Args:
        session: (DBSession)
        project: (Project) an already existing project
        name: (str) name of the interface

    Returns:
        (Interface)
    """
    cnt = _ensure_project_content(session, project)

    item = Interface(id=uuid1().hex, cnt=cnt.id, name=name)
    session.add(item)

    return item


def create_notebook(session, project, name):
    """Create a new notebook description and associate it to a project.

    Args:
        session: (DBSession)
        project: (Project) an already existing project
        name: (str) name of the notebook

    Returns:
        (Notebook)
    """
    cnt = _ensure_project_content(session, project)

    notebook = Notebook(id=uuid1().hex, cnt=cnt.id, name=name)
    session.add(notebook)

    return notebook


def create_workflow_node(session, project, node_def):
    """Create a new node description and associate it to a project.

    Args:
        session: (DBSession)
        project: (Project) an already existing project
        node_def: (dict of node prop) node definition

    Returns:
        (WorkflowNode)
    """
    cnt = _ensure_project_content(session, project)

    node = WorkflowNode(id=node_def['id'],
                        cnt=cnt.id,
                        name=node_def['name'])
    session.add(node)
    node.store_description(node_def['description'])
    node.store_definition(node_def)

    return node


def create_workflow(session, project, workflow_def):
    """Create a new workflow description and associate it to a project.

    Args:
        session: (DBSession)
        project: (Project) an already existing project
        workflow_def: (dict of (str, any)) workflow definition

    Returns:
        (Workflow)
    """
    cnt = _ensure_project_content(session, project)

    workflow = Workflow(id=workflow_def['id'],
                        cnt=cnt.id,
                        name=workflow_def['name'])
    session.add(workflow)
    workflow.store_description(workflow_def['description'])
    workflow.store_definition(workflow_def)

    return workflow


def clear_project_content(session, project):
    """Remove all items in project content and delete content object.

    Args:
        session: (DBSession)
        project: (Project)

    Returns:
        None
    """
    cnt = Content.get(session, project.id)
    if cnt is None:
        return

    for item_typ in item_types:
        for item in getattr(cnt, item_typ):
            session.delete(item)

    session.delete(cnt)
