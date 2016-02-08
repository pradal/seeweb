"""Default API for source providers
"""
import os
from os.path import exists


def fetch_sources(src_url, dst):
    """Fetch sources located in src_url
    and copy them into a pid directory in dst.

    Args:
        src_url: (str) a valid url to fetch sources from
        dst: (str) a local path to copy files in

    Returns:
        (bool): whether sources have been retrieved or not
    """
    del src_url

    if not exists(dst):
        os.mkdir(dst)

    return True
