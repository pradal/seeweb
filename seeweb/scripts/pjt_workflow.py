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

    idef = dict(id='any',
                name='any',
                author="revesansparole",
                description="Any type of data",
                version=0,
                schema={},
                ancestors=[]
                )
    ContentItem.create_from_def(session, "interface", idef, nodelib)

    idef = dict(id='int',
                name='int',
                author="revesansparole",
                description="integer type",
                version=0,
                schema={"type": "integer"},
                ancestors=[]
                )
    ContentItem.create_from_def(session, "interface", idef, nodelib)

    idef = dict(id='float',
                name='float',
                author="revesansparole",
                description="float type",
                version=0,
                schema={"type": "number"},
                ancestors=[]
                )
    ContentItem.create_from_def(session, "interface", idef, nodelib)

    idef = dict(id='str',
                name='string',
                author="revesansparole",
                description="string type",
                version=0,
                schema={"type": "string"},
                ancestors=[]
                )
    ContentItem.create_from_def(session, "interface", idef, nodelib)

    ndefs = []
    for i in range(3):
        node_def = dict(id=uuid1().hex,
                        name="read%d" % i,
                        description="toto was here",
                        author="revesansparole",
                        version=0,
                        function="testio:read",
                        inputs=[dict(name="in1", interface="int",
                                     default="0", description="counter"),
                                dict(name="in2", interface="str",
                                     default="a", description="unit")],
                        outputs=[dict(name="ret", interface="int",
                                      description="important result")])

        ContentItem.create_from_def(session, "workflow_node", node_def, nodelib)
        ndefs.append(node_def)

    alias = ContentItem.create(session, uuid1().hex, "alias", nodelib)
    alias.author = "revesansparole"
    alias.name = ndefs[2]['id']

    workflow = Project.create(session, 'revesansparole', 'workflow')
    workflow.public = True

    workflow_def = dict(id=uuid1().hex,
                        name="sample_workflow",
                        description="trying some stuff",
                        author="revesansparole",
                        version=0,
                        nodes=[dict(id=ndefs[0]['id'], label="node1",
                                    x=-50, y=-80),
                               dict(id=ndefs[1]['id'], label=None,
                                    x=50, y=-80),
                               dict(id=alias.id, label=None,
                                    x=0, y=0),
                               dict(id=uuid1().hex, label="fail",
                                    x=0, y=80)],
                        links=[(0, "ret", 2, "in1"),
                               (1, "ret", 2, "in2"),
                               (2, "ret", 3, "in")])

    ContentItem.create_from_def(session, "workflow", workflow_def, workflow)
