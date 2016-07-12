from uuid import uuid1

from seeweb.models.ro_link import ROLink
from seeweb.ro.container.models.ro_container import ROContainer
from seeweb.ro.interface.models.ro_interface import ROInterface
from seeweb.ro.workflow_node.models.ro_workflow_node import ROWorkflowNode


def main(session, user):
    """Create workflow related projects.

    Args:
        session (DBSession):
        user (User): owner of created project

    Returns:
        None
    """
    roc = ROContainer()
    roc.init(session, dict(creator=user.id, title="nodelib"))

    for iname in ("any", "IStr", "IInt", "IFileStr"):
        roi = ROInterface()
        roi.init(session, dict(creator=user.id, title=iname))

        ROLink.connect(session, roc.id, roi.id, "contains")

    rown = ROWorkflowNode()
    rown.init(session, dict(creator=user.id, title="node"))
    ROLink.connect(session, roc.id, rown.id, "contains")
