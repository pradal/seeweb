"""Set of functions to explore the content of a project i.e. its sources
"""
from os import walk
from os.path import join as pj

from seeweb.models.project_content.notebook import Notebook
from seeweb.models.project_content.workflow import Workflow
from seeweb.models.project_content.workflow_node import WorkflowNode
from seeweb.project.source import has_source, source_pth

import notebook
import workflow_node
import workflow


fac = dict(notebook=(notebook, Notebook.create),
           workflow=(workflow, Workflow.create),
           workflow_node=(workflow_node, WorkflowNode.create))


def explore_sources(session, project):
    """Explore source files associated to a project.

    Fill project content with all elements recognized
    by the platform.

    Args:
        session: (DBSession)
        project: (Project)

    Returns:
        None
    """
    if not has_source(project.id):
        print "nothing"
        return

    pth = source_pth(project.id).replace("\\", "/")

    project.clear_content(session)
    n = len(pth)

    for root, dirnames, filenames in walk(pth):
        # avoid hidden directories
        for i in range(len(dirnames) - 1, -1, -1):
            if dirnames[i].startswith("."):
                del dirnames[i]

        dname = root.replace("\\", "/")[n:]
        print dname

        # find recognized content items
        for fname in filenames:
            pth = pj(root, fname)
            for item_type, (mod, create) in fac.items():
                if mod.can_handle_file(pth):
                    item = mod.analyse(pth)
                    create(session, project, item)

    # for executable in find_executables(project.id):
    #     create_executable(session, project, executable)
    #
    # for notebook in find_notebooks(project.id):
    #     create_notebook(session, project, notebook[1])
    #
    # for node in find_workflow_nodes(project.id):
    #     WorkflowNode.create(session, project, node['name'])
    #
    # for workflow in find_workflows(project.id):
    #     Workflow.create(session, project, workflow['name'])
