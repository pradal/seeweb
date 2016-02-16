import json
from sqlalchemy import Column, String, Text

from seeweb.models.described import Described


class ContentItem(Described):
    """Base class for content items.
    """
    id = Column(String(32), nullable=False, primary_key=True)
    name = Column(String(255), nullable=False)
    definition = Column(Text, default="")

    def store_definition(self, obj):
        """Serialize obj in json format to store it as def.

        Args:
            obj: (any) any json serializable object

        Returns:
            None
        """
        self.definition = json.dumps(obj)

    def load_definition(self):
        """Load previously stored definition.

        Returns:
            (any): any json serialized object stored.
        """
        if self.definition == "":
            return None

        return json.loads(self.definition)
