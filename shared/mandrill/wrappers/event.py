from shared.mandrill.wrappers.attachments import MandrillAttachmentWrapper


class MsgKeyMissingError(AssertionError):
    pass


class MandrillEventWrapper(object):
    """Convenience wrapper around the JSON representation of a single email event in Mandrill POST data."""

    def __init__(self, event_json):
        self.event_json = event_json

        self.ts = event_json.get('ts')

        if not 'msg' in self.event_json:
            raise MsgKeyMissingError(u'data does not contain a msg key')

        self.raw_msg = self.event_json['msg']['raw_msg']

        self.email = self.event_json['msg']['email']  # the email to which the events were sent

        self.subject = self.event_json['msg']['subject']

        self.text_flowed = self.event_json['msg']['text_flowed']
        self.tags = self.event_json['msg']['tags']
        self.template = self.event_json['msg']['template']
        self.spam_report = self.event_json['msg']['spam_report']
        self.headers = self.event_json['msg']['headers']
        self.dkim = self.event_json['msg']['dkim']
        self.spf = self.event_json['msg']['spf']

        self.from_name = self.event_json['msg']['from_name']
        self.from_email = self.event_json['msg']['from_email']

        self.sender = self.event_json['msg']['sender']
        self.to = self.event_json['msg']['to']

        self.text = self.event_json['msg']['text']
        self.html = self.event_json['msg']['html']

        self.attachments = extract_attachments(self.event_json['msg']['attachments'])


def extract_attachments(attachment_json):
    """

    Args:
        attachment_json (json):

    Returns (list): list of MandrillAttachmentWrapper instances

    """
    attachments = []

    for file_name, file_data in attachment_json.items():
        attachment = MandrillAttachmentWrapper(file_name, file_data)
        attachments.append(attachment)

    return attachments
