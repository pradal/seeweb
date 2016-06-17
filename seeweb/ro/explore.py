from dateutil.parser import parse
import json
from uuid import uuid1

from seeweb.models.research_object import ResearchObject
from seeweb.ro.article.models.ro_article import ROArticle


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
            ro_type = ro_def.get("type", 'ro')
            return ro_type
    except ValueError:
        return None


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

    data["creation"] = parse(data["creation"])
    uid = uuid1().hex#data["id"]

    if ro_type == 'article':
        ro = ROArticle.create(session, uid, data["creator"], data["title"])
    else:
        ro = ResearchObject.create(session, uid, data["creator"], data["title"])

    ro.store_description(data['description'])

    return ro
