from seeweb.models.ro_link import ROLink
from seeweb.ro.container.models.ro_container import ROContainer
from seeweb.ro.interface.models.ro_interface import ROInterface
from seeweb.ro.workflow_node.models.ro_workflow_node import ROWorkflowNode
from seeweb.ro.workflow.models.ro_workflow import ROWorkflow


def main(session, user):
    """Create workflow related projects.

    Args:
        session (DBSession):
        user (User): owner of created project

    Returns:
        None
    """
    roc = ROContainer()
    roc.init(session, dict(creator=user.id, name="nodelib"))

    for iname in ("any", "IBool", "ICodeStr", "IColor", "IData", "IDateTime",
                  "IDict", "IDirStr",
                  "IEnumStr", "IFileStr", "IFloat",
                  "IFunction", "IInt", "IRGBColor",
                  "ISequence", "ISlice", "IStr", "ITextStr",
                  "ITuple", "ITuple3"):
        roi = ROInterface()
        roi.init(session, dict(creator=user.id, name=iname))

        ROLink.connect(session, roc.id, roi.id, "contains")

    rown = ROWorkflowNode()
    rown.init(session, dict(creator=user.id, name="node"))
    ROLink.connect(session, roc.id, rown.id, "contains")

    row = ROWorkflow()
    row.init(session, dict(creator=user.id, name="workflow"))
    ROLink.connect(session, roc.id, row.id, "contains")
