from PIL import Image

from seeweb.avatar import upload_user_avatar
from seeweb.models.auth import Role
from seeweb.models.ro_link import ROLink
from seeweb.models.user import User

from seeweb.ro.article.models.ro_article import ROArticle
from seeweb.ro.container.models.ro_container import ROContainer


def main(session, user, container):
    """Create ROs to test auth policies.

    Args:
        session (DBSession):
        user (User): default user
        container (ROContainer): top level container

    Returns:
        None
    """
    # create another user
    other = User.create(session,
                        uid='other',
                        name="Other User",
                        email="other@email.com")

    img = Image.open("seeweb/scripts/avatar/sartzet.png")
    upload_user_avatar(img, other)

    # user can view RO in container owner by other
    roa = ROArticle()
    roa.init(session, dict(owner=other.id, name="other article"))
    roa.store_description("Title\n=====\n\nLorem Ipsum\nlorem ipsum")
    roa.add_policy(session, user, Role.view)

    road = ROArticle()
    road.init(session, dict(owner=other.id, name="other editable article"))
    road.store_description("Title\n=====\n\nLorem Ipsum\nlorem ipsum")
    road.add_policy(session, user, Role.edit)

    roc = ROContainer()
    roc.init(session, dict(owner=other.id,
                           name="other project",
                           contents=[roa, road]))
    ROLink.connect(session, container.id, roc.id, 'contains')

    # access granted to ROs through their container policy
    roa = ROArticle()
    roa.init(session, dict(owner=other.id, name="other 'private' article"))
    roa.store_description("Title\n=====\n\nLorem Ipsum\nlorem ipsum")

    roc = ROContainer()
    roc.init(session, dict(owner=other.id,
                           name="other 'denied' project",
                           contents=[roa]))
    roc.add_policy(session, user, Role.denied)
    ROLink.connect(session, container.id, roc.id, 'contains')

    roc = ROContainer()
    roc.init(session, dict(owner=other.id,
                           name="other project",
                           contents=[roa]))
    roc.add_policy(session, user, Role.edit)
    ROLink.connect(session, container.id, roc.id, 'contains')

    # public container
    roa = ROArticle()
    roa.init(session, dict(owner=other.id, name="other article"))
    roa.store_description("Title\n=====\n\nLorem Ipsum\nlorem ipsum")

    road = ROArticle()
    road.init(session, dict(owner=other.id, name="other denied article"))
    road.store_description("Title\n=====\n\nLorem Ipsum\nlorem ipsum")
    road.add_policy(session, user, Role.denied)

    roc = ROContainer()
    roc.init(session, dict(owner=other.id,
                           name="other 'public' project",
                           contents=[roa, road]))
    roc.public = True
    ROLink.connect(session, container.id, roc.id, 'contains')
