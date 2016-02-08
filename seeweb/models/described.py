from docutils.core import publish_parts
from sqlalchemy import Column, Text


class Described(object):
    """Abstract class used for all objects with a description
    """
    description = Column(Text, default="")

    def html_description(self):
        """Convert restructured text into html

        Returns:
            (str) html value of the description
        """
        if self.description == "":
            return ""
        else:
            try:
                html = publish_parts(self.description,
                                     writer_name='html')['html_body']
            except AttributeError as e:
                html = "<body>Error %s</body>" % str(e)

            return html

    def store_description(self, rst):
        """Sanitize input text and store it as description

        Args:
            rst: (str) restructured text value of the description

        Returns:
            None
        """
        if rst is None:
            rst = ""

        self.description = str(rst)
