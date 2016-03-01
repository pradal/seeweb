from uuid import uuid1

from seeweb.models.content_item import ContentItem
from seeweb.models.project import Project


def main(session):
    """Create script related projects.

    Args:
        session: (DBSession)

    Returns:
        None
    """
    pjt = Project.create(session, 'revesansparole', 'script_lib')
    pjt.public = True

    idef = dict(id=uuid1().hex,
                name='example',
                author="revesansparole",
                description="Compute some random values",
                version=0,
                language="python",
                source="""
from random import random

sample = [random() for i in range(3)]
print sample

                """
                )
    ContentItem.create_from_def(session, "script", idef, pjt)

    idef = dict(id=uuid1().hex,
                name='fail',
                author="revesansparole",
                description="Raise an exception",
                version=0,
                language="python",
                source="""
from random import random

sample = [random() for i in range(3)]
print sample

raise UserWarning("Fail is in the air")
                """
                )
    ContentItem.create_from_def(session, "script", idef, pjt)

    idef = dict(id=uuid1().hex,
                name='long',
                author="revesansparole",
                description="Sleep throughout execution",
                version=0,
                language="python",
                source="""
from random import random
from time import sleep

sample = [random() for i in range(3)]
print sample

sleep(3)
print [v * 2 for v in sample]
                """
                )
    ContentItem.create_from_def(session, "script", idef, pjt)

    idef = dict(id=uuid1().hex,
                name='Rscript',
                author="revesansparole",
                description="More statistic oriented analysis",
                version=0,
                language="R",
                source="""
# Define a variable.
x <- rnorm(10)

# calculate the mean of x and print out the results.
mux = mean(x)
cat("The mean of x is ",mean(x),"\\n")

# print out a summary of the results
summary(x)
cat("The summary of x is \\n",summary(x),"\\n")
print(summary(x))
                """
                )
    ContentItem.create_from_def(session, "script", idef, pjt)

