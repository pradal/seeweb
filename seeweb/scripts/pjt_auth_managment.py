from PIL import Image

from seeweb.avatar import upload_user_avatar
from seeweb.models.ro_link import ROLink
from seeweb.models.user import User

from seeweb.ro.article.models.ro_article import ROArticle
from seeweb.ro.container.models.ro_container import ROContainer


def main(session, user):
    """Create ROs to test auth policies.

    Args:
        session (DBSession):
        user (User): default user

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

