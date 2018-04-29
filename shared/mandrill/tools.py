import json

import arrow
from django.db import transaction
from shared.constants import MIME_TYPE_TEXT_PLAIN
from shared.email.models import EmailMessage, EmailAttachment
from shared.email.tools import get_or_create_email_address
from shared.file_storage.tools import put_file
from shared.mandrill.wrappers.transmission import MandrillTransmissionWrapper
from shared.tools import convert_string_content_to_stream

VALID_ATTACHMENT_FILETYPES = {
    'text/plain': u'.txt',
    'application/msword': '.doc',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': u'.docx',
    'application/pdf': u'.pdf'
}

class InvalidAttachmentFileTypeError(AssertionError):
    def __init__(self, mime_type):
        self.mime_type = mime_type
        supported_mime_type_string = u', '.join(VALID_ATTACHMENT_FILETYPES.keys())
        message = u'{} is not a supported mime type for attachments. ' \
                  u'Supported mime types are: {}'.format(
            mime_type, supported_mime_type_string)
        super(InvalidAttachmentFileTypeError, self).__init__(message)


def get_sender_emails(data):
    if 'mandrill_events' not in data:
        raise ValueError(u'invalid data')
    try:
        mandrill_events = json.loads(data.get('mandrill_events'))
    except ValueError as e:
        raise ValueError(u'mandrill events not supplied as valid JSON')

    return [mandrill_event['msg']['email'] for mandrill_event in mandrill_events]


@transaction.atomic
def save_raw_email_message(data, agent=None):
    content = convert_string_content_to_stream(data)
    datetime_string = arrow.utcnow().format('YYYY-MM-DD_HH-mm-ss')
    return put_file(
        u'incoming_mail/{}/email_content.txt'.format(datetime_string), content, mime_type=MIME_TYPE_TEXT_PLAIN)


@transaction.atomic
def persist_email_messages(json_data):
    transmission = MandrillTransmissionWrapper(json_data)
    email_messages = []
    for event in transmission.events:
        email_messages.append(persist_event(event))
    return email_messages


@transaction.atomic
def persist_event(event):
    email_address_sender = get_or_create_email_address(event.from_email, event.from_name)

    fields = {
        'sender': email_address_sender,
        'text': event.text,
        'html': event.html,
    }
    email_message = EmailMessage(**fields)
    email_message.save()

    for recipient_info in event.to:
        email_address = get_or_create_email_address(
            recipient_info[0], email_name=recipient_info[1])
        email_message.recipients.add(email_address)

    persist_attachments(email_message, event.attachments)

    return email_message


@transaction.atomic
def persist_attachments(email_message, attachments):
    persisted_attachments = []
    for attachment in attachments:
        try:
            file_reference = persist_attachment(email_message, attachment)
            email_attachment = EmailAttachment(
                email_message=email_message, file_reference=file_reference)
            email_attachment.save()
            persisted_attachments.append(email_attachment)
        except InvalidAttachmentFileTypeError:
            pass
    return persisted_attachments


@transaction.atomic
def persist_attachment(email_message, attachment):
    if not attachment.type in VALID_ATTACHMENT_FILETYPES:
        raise InvalidAttachmentFileTypeError(attachment.type)
    file_object = attachment.get_file_object()
    path = u'emails/{}/attachments/{}'\
        .format(email_message.pk, attachment.file_name)
    return put_file(path, file_object, mime_type=attachment.type)
