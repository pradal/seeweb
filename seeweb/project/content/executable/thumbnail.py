"""Set of functions to explore the content of a project i.e. its sources
"""
from PIL import Image, ImageDraw, ImageFont


def create_thumbnail(item, **kwds):
    """Create thumbnail associated to some content item.

    Args:
        item: (ContentItem)
        kwds: (dict of any) extra parameters

    Returns:
        Image or None if no thumbnail can be generated
    """
    img = Image.new("RGBA", (512, 512), "green")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf", 240)
    draw.text((100, 100), "exe", fill="blue", font=font)

    return img
