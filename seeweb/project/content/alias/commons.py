from seeweb.models.content_item import ContentItem


def resolve_target(session, alias):
    """Find the first ancestor of alias which is not an alias

    Args:
        session: (DBSession)
        alias: (ContentItem) category == 'alias'

    Returns:
        (ContentItem) category != 'alias'
    """
    tgt = ContentItem.get(session, alias.name)
    if tgt is None:
        return None
    elif tgt.category == 'alias':
        return resolve_target(session, tgt)
    else:
        return tgt
