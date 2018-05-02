from django.test import TestCase
from django.test.utils import override_settings
from mock import patch
from shared.email.wrapper import EmailWrapper


class TestEmailWrapper(TestCase):

    @patch('shared.email.wrapper.EmailWrapper.render_template')
    @patch('shared.email.wrapper.EmailWrapper.send_email_message')
    def test_email_wrapper(self, mock_send_email_message, mock_render_template):
        test_sender_email = u'noreply@test.de'
        test_email_content = u'TEST'
        mock_render_template.return_value = test_email_content

        with override_settings(DEFAULT_EMAIL_SENDER=test_sender_email):
            email_wrapper = EmailWrapper()
            email_wrapper.send(recipients=[u'a@a.de', u'b@b.de'], cc=[u'c@c.de'], bcc=[u'd@d.de'])

        self.assertDictEqual(mock_render_template.mock_calls[0][2], {u'extension': u'txt'})
        self.assertDictEqual(mock_render_template.mock_calls[1][2], {u'extension': u'html'})

        mock_send_email_message.assert_called_with(
            alternatives=None,
            attachments=None,
            bcc=[u'd@d.de'],
            cc=[u'c@c.de'],
            connection=None,
            fail_silently=False,
            from_email=test_sender_email,
            headers=None,
            html=test_email_content,
            reply_to=None,
            subject=None,
            text=test_email_content,
            to=[u'a@a.de', u'b@b.de'])
