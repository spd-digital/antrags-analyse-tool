# coding=utf-8
import json

from django.test.testcases import TestCase
from freezegun import freeze_time
from mock.mock import MagicMock, patch
from model_mommy import mommy
from shared.email.model_factories import EmailMessageFactory
from shared.email.models import EmailAttachment
from shared.file_storage.models import FileReference
from shared.mandrill.tools import InvalidAttachmentFileTypeError, get_sender_emails, save_raw_email_message, \
    persist_email_messages, persist_event, persist_attachments, persist_attachment


class TestInvalidAttachmentFileTypeError(TestCase):
    def test_exception(self):
        exc = InvalidAttachmentFileTypeError(u'application/java-archive')
        expected_message = u'application/java-archive is not a supported mime type for attachments. ' \
                           u'Supported mime types are: application/pdf, ' \
                           u'application/vnd.openxmlformats-officedocument.wordprocessingml.document, ' \
                           u'text/plain, application/msword'
        self.assertEqual(exc.message, expected_message)


class TestGetSenderEmails(TestCase):

    def test_no_events(self):
        with self.assertRaises(ValueError) as e:
            get_sender_emails({})
        self.assertEqual(e.exception.message, u'invalid data')

    def test_invalid_json(self):
        with self.assertRaises(ValueError) as e:
            get_sender_emails({'mandrill_events': MagicMock(name=u'definitely_not_json_serializable')})
        self.assertEqual(e.exception.message, u'mandrill events not supplied as valid JSON')

    def test_get_sender_emails(self):
        actual_sender_emails = get_sender_emails({
            'mandrill_events': json.dumps([
                {'msg': {'email': 'august@spd.de'}},
                {'msg': {'email': 'wilhelm@spd.de'}}
            ])
        })
        self.assertEqual(len(actual_sender_emails), 2)
        self.assertIn('august@spd.de', actual_sender_emails)
        self.assertIn('wilhelm@spd.de', actual_sender_emails)


class TestSaveEmailMessage(TestCase):

    @freeze_time('2018-05-19 12:21:00')
    @patch('shared.mandrill.tools.put_file')
    @patch('shared.mandrill.tools.convert_string_content_to_stream')
    def test_save_raw_email_message(self, mock_convert_string_content_to_stream, mock_put_file):
        mock_stream = MagicMock()
        mock_convert_string_content_to_stream.return_value = mock_stream

        save_raw_email_message(MagicMock())

        mock_put_file.assert_called_with(
            u'incoming_mail/2018-05-19_12-21-00/email_content.txt', mock_stream, mime_type=u'text/plain')


class TestPersistEmailMessages(TestCase):

    @patch('shared.mandrill.tools.persist_event')
    @patch('shared.mandrill.tools.MandrillTransmissionWrapper')
    def test_persist_email_messages(self, MockMandrillTransmissionWrapper, mock_persist_event):
        mock_transmission = MagicMock()
        mock_event1 = MagicMock()
        mock_event2 = MagicMock()
        mock_event3 = MagicMock()
        mock_transmission.events = [mock_event1, mock_event2, mock_event3]
        MockMandrillTransmissionWrapper.return_value = mock_transmission

        mock_persist_event.side_effect = lambda x: MagicMock(payload=x)

        email_messages = persist_email_messages(MagicMock(name=u'mock_json_data'))

        self.assertEqual(email_messages[0].payload, mock_event1)
        self.assertEqual(email_messages[1].payload, mock_event2)
        self.assertEqual(email_messages[2].payload, mock_event3)


class TestPersistEvent(TestCase):

    @patch('shared.mandrill.tools.persist_attachments')
    @patch('shared.mandrill.tools.EmailMessage')
    @patch('shared.mandrill.tools.get_or_create_email_address')
    def test_persist_event(self, mock_get_or_create_email_address, MockEmailMessage, mock_persist_attachments):
        mock_event = MagicMock(
            from_email=u'rosa.luxemburg@generalstreik.de',
            from_name=u'Rosa Luxemburg',
            to=[u'karl.kautsky@dieneuezeit.de', u'mitglieder@spd.de'],
            text=u'Ich komme infolge meiner mündlichen Agitation mit erheblicher Verspätung dazu, '
                 u'dem Genossen Kautsky zu antworten',
            html=u'<p>Ich komme infolge meiner mündlichen Agitation mit erheblicher Verspätung dazu, '
                 u'dem Genossen Kautsky zu antworten</p>',
            attachments=[MagicMock(name='attachment')]
        )

        mock_get_or_create_email_address.side_effect = lambda email, **kwargs: MagicMock(email=email, **kwargs)

        mock_email_message = MagicMock()
        def update_email_message(mock_email_message, *args, **kwargs):
            mock_email_message.__dict__.update(**kwargs)
            return mock_email_message
        MockEmailMessage.side_effect = lambda *args, **kwargs: update_email_message(mock_email_message, *args, **kwargs)

        actual_email_message = persist_event(mock_event)

        mock_persist_attachments.assert_called_with(mock_email_message, mock_event.attachments)
        self.assertEqual(len(mock_email_message.recipients.add.mock_calls), 2)


class TestPersistAttachments(TestCase):

    def setUp(self):
        self.email_message = EmailMessageFactory()
        self.attachments = [
            MagicMock(file_name=u'mock_mandrill_attachment_wrapper_1.pdf'),
            MagicMock(file_name=u'mock_mandrill_attachment_wrapper_2.pdf'),
            MagicMock(file_name=u'mock_mandrill_attachment_wrapper_3.pdf')
        ]

    @patch('shared.mandrill.tools.persist_attachment')
    def test_persist_attachments(self, mock_persist_attachment):
        mock_persist_attachment.side_effect = lambda email_message, attachment: mommy.make(
            FileReference, file_name=attachment.file_name)

        persist_attachments(self.email_message, self.attachments)

        self.assertEqual(FileReference.objects.count(), 5) # 3 + 2 due to factory

        for attachment in self.attachments:
            try:
                file_reference = FileReference.objects.get(file_name=attachment.file_name)
            except FileReference.DoesNotExist:
                raise AssertionError(u'missing file reference for attachment {}'.format(attachment.file_name))

            try:
                EmailAttachment.objects.get(email_message=self.email_message, file_reference=file_reference)
            except EmailAttachment.DoesNotExist:
                raise AssertionError(u'missing email attachment for attachment {}'.format(attachment.file_name))


class TestPersistAttachment(TestCase):

    def setUp(self):
        self.email_message = EmailMessageFactory()

    def test_type_invalid(self):
        with self.assertRaises(InvalidAttachmentFileTypeError) as e:
            persist_attachment(self.email_message, MagicMock(type=u'mimetype/definitely.invalid'))
        expected_exception_message = \
            u'mimetype/definitely.invalid is not a supported mime type for attachments. ' \
            u'Supported mime types are: application/pdf, ' \
            u'application/vnd.openxmlformats-officedocument.wordprocessingml.document, text/plain, application/msword'
        self.assertEqual(e.exception.message, expected_exception_message)

    @patch('shared.mandrill.tools.put_file')
    def test_persist_attachment(self, mock_put_file):
        mock_attachment = MagicMock(file_name=u'Luxemburg_Ermattung_oder_Kampf.pdf', type=u'application/pdf')
        mock_file_object = MagicMock()
        mock_attachment.get_file_object.return_value = mock_file_object

        persist_attachment(self.email_message, mock_attachment)

        mock_put_file.assert_called_with(u'emails/{}/attachments/Luxemburg_Ermattung_oder_Kampf.pdf'.format(
            self.email_message.pk), mock_file_object, mime_type=u'application/pdf')
