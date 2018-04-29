from base64 import b64decode
from io import BytesIO


class MandrillAttachmentWrapper(object):

    def __init__(self, file_name, file_data):
        self.file_name = file_name
        self.file_data = file_data

        self.name = file_data.get(u'name')
        self.type = file_data.get(u'type')
        self.base64 = file_data.get(u'base64')
        self.content = file_data.get(u'content')

    def get_file_object(self):
        return BytesIO(b64decode(self.content))
