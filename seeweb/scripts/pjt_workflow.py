from uuid import uuid1

from seeweb.models.content_item import ContentItem
from seeweb.models.project import Project


def main(session):
    """Create workflow related projects.

    Args:
        session: (DBSession)

    Returns:
        None
    """
    nodelib = Project.create(session, 'revesansparole', 'nodelib')
    nodelib.public = True

    item = ContentItem.create(session, uuid1().hex, "interface", nodelib)
    item.name = "IInt"
    item = ContentItem.create(session, uuid1().hex, "interface", nodelib)
    item.name = "IStr"

    ndefs = []
    for i in range(3):
        node_def = dict(id=uuid1().hex,
                        name="read%d" % i,
                        category="oanode",
                        description="toto was here",
                        author="revesansparole",
                        function="testio:read",
                        inputs=[dict(name="in1", interface="IInt",
                                     value="0", descr="counter"),
                                dict(name="in2", interface="IStr",
                                     value="a", descr="unit")],
                        outputs=[dict(name="ret", interface="IInt",
                                      descr="important result")])

        item = ContentItem.create(session, node_def['id'],
                                  "workflow_node", nodelib)
        item.name = node_def['name']
        item.author = node_def['author']
        item.store_definition(node_def)
        ndefs.append(node_def)

    workflow = Project.create(session, 'revesansparole', 'workflow')
    workflow.public = True

    workflow_def = dict(id=uuid1().hex,
                        name="sample_workflow",
                        category="oaworkflow",
                        description="trying some stuff",
                        author="revesansparole",
                        nodes=[dict(id=ndefs[0]['id'], label="node1",
                                    x=-50, y=-80),
                               dict(id=ndefs[1]['id'], label=None,
                                    x=50, y=-80),
                               dict(id=ndefs[2]['id'], label=None,
                                    x=0, y=0),
                               dict(id=uuid1().hex, label="fail",
                                    x=0, y=80)],
                        connections=[(0, "ret", 2, "in1"),
                                     (1, "ret", 2, "in2"),
                                     (2, "ret", 3, "in")])

    item = ContentItem.create(session, workflow_def['id'],
                              "workflow", workflow)
    item.name = workflow_def['name']
    item.author = workflow_def['author']
    item.store_definition(workflow_def)
