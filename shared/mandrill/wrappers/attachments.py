from base64 import b64decode
from io import BytesIO


class MandrillAttachmentWrapper(object):
    """Convenience wrapper around the JSON representation of a single attachment in Mandrill POST data."""

    def __init__(self, file_name, file_data):
        self.file_name = file_name # file name, ex: 2018-04-22_Antrag-291a.pdf
        self.file_data = file_data # Mandrill's JSON representation of the attachment

        self.name = file_data.get(u'name') # file name, ex: 2018-04-22_Antrag-291a.pdf (redundant)
        self.type = file_data.get(u'type') # mime type, ex: application/pdf
        self.base64 = file_data.get(u'base64') # boolean: is the attachment content base64 encoded?
        self.content = file_data.get(u'content') # unicode: the attachment content

    def get_file_object(self):
        """Transform the base64 encoded content of the attachment into a bytes stream.

        Returns (BytesIO): a bytes stream

        """
        return BytesIO(b64decode(self.content))
