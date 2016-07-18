from uuid import uuid1

from seeweb.models.ro_link import ROLink
from seeweb.ro.container.models.ro_container import ROContainer
from seeweb.ro.interface.models.ro_interface import ROInterface
from seeweb.ro.workflow.models.ro_workflow import ROWorkflow
from seeweb.ro.workflow_node.models.ro_workflow_node import ROWorkflowNode
from seeweb.ro.workflow_prov.models.ro_workflow_prov import ROWorkflowProv


def main(session, user):
    """Create workflow related projects.

    Args:
        session (DBSession):
        user (User): owner of created project

    Returns:
        None
    """
    # default interfaces for openalea
    roa = ROContainer()
    roa.init(session, dict(owner=user.id, name="openalea.interfaces"))

    for iname in ("any", "IBool", "ICodeStr", "IColor", "IData", "IDateTime",
                  "IDict", "IDirStr",
                  "IEnumStr", "IFileStr", "IFloat",
                  "IFunction", "IInt", "IRGBColor",
                  "ISequence", "ISlice", "IStr", "ITextStr",
                  "ITuple", "ITuple3"):
        roi = ROInterface()
        roi.init(session, dict(owner=user.id, name=iname))

        ROLink.connect(session, roa.id, roi.id, "contains")

    roc = ROContainer()
    roc.init(session, dict(owner=user.id, name="nodelib"))

    ndefs = []
    for i in range(3):
        node_def = dict(name="read%d" % i,
                        description="toto was here",
                        author=user.id,
                        function="testio:read",
                        inputs=[dict(name="in1", interface="IInt",
                                     default="0", description="counter"),
                                dict(name="in2", interface="IStr",
                                     default="a", description="unit")],
                        outputs=[dict(name="ret", interface="IInt",
                                      description="important result")])

        rown = ROWorkflowNode()
        rown.init(session, node_def)
        ndefs.append(rown)

        ROLink.connect(session, roc.id, rown.id, "contains")

    # alias = ContentItem.create(session, uuid1().hex, "alias", nodelib)
    # alias.author = "revesansparole"
    # alias.name = ndefs[2]['id']

    workflow_def = dict(name="sample_workflow",
                        description="trying some stuff",
                        author="revesansparole",
                        nodes=[dict(id=ndefs[0].id, label="node1",
                                    x=-50, y=-80),
                               dict(id=ndefs[1].id, label=None,
                                    x=50, y=-80),
                               dict(id=ndefs[2].id, label=None,
                                    x=0, y=0),
                               dict(id='4094cf5a490711e6aa4cd4bed973e64a',
                                    label="fail",
                                    x=0, y=80)],
                        links=[dict(source=0, source_port="ret",
                                    target=2, target_port="in1"),
                               dict(source=1, source_port="ret",
                                    target=2, target_port="in2"),
                               dict(source=2, source_port="ret",
                                    target=3, target_port="in")])

    row = ROWorkflow()
    row.init(session, workflow_def)
    ROLink.connect(session, roc.id, row.id, "contains")

    roc = ROContainer()
    roc.init(session, dict(owner=user.id, name="provenance"))

    data = [dict(id=uuid1().hex, type="int", value=1),
            dict(id=uuid1().hex, type="int", value=10),
            dict(id=uuid1().hex, type="str", value="Killroy was here")
            ]

    prov_def = dict(name="sample_provenance",
                    description="trying some stuff",
                    author=user.id,
                    workflow=row.id,
                    time_init=10,
                    time_end=11,
                    data=data,
                    parameters=[dict(node=0, port="in1", data=data[0]['id']),
                                dict(node=0, port="in2", data=data[2]['id'])
                                ],
                    executions=[
                        dict(node=0, time_init=10, time_end=11,
                             inputs=[
                                 {"port": "in1", "data": data[0]['id']},
                                 {"port": "in2", "data": data[2]['id']}
                             ],
                             outputs=[
                                 {"port": "ret", "data": data[1]['id']}
                             ]),
                        dict(node=1, time_init=10, time_end=11,
                             inputs=[
                                 {"port": "in1", "data": data[0]['id']}
                             ],
                             outputs=[
                                 {"port": "ret", "data": data[1]['id']}
                             ])
                    ]
                    )

    rop = ROWorkflowProv()
    rop.init(session, prov_def)
    ROLink.connect(session, roc.id, rop.id, "contains")
