from accounts.models import UserAccount
from django.test.testcases import TestCase
from mock import patch, MagicMock
from propositions.models import ProtoProposition
from propositions.processes.submit_by_email import submit_proposition_by_email, submit_proposition_by_emails
from shared.email.model_factories import EmailMessageFactory


class TestSubmitPropositionByEmails(TestCase):

    @patch('propositions.processes.submit_by_email.submit_proposition_by_email')
    def test_submit_proposition_by_emails(self, mock_submit_proposition_by_email):
        test_email_messages = [MagicMock(), MagicMock()]
        submit_proposition_by_emails(test_email_messages)
        self.assertEqual(len(mock_submit_proposition_by_email.mock_calls), 2)


class TestSubmitPropositionByEmail(TestCase):

    def setUp(self):
        self.email_message = EmailMessageFactory()

    @patch('accounts.tools.generate_password')
    @patch('shared.email.wrapper.EmailWrapper.send_email_message')
    def test_submit_proposition_by_email(self, mock_send_email_message, mock_generate_password):
        expected_password = u'opensesame'

        mock_generate_password.return_value = expected_password

        submit_proposition_by_email(self.email_message)

        # user account should exist
        try:
            user_account = UserAccount.objects.get(user__email=self.email_message.sender.address)
        except UserAccount.DoesNotExist:
            raise AssertionError(u'user account does not exist')

        # proto proposition should exist
        try:
            proto_proposition = ProtoProposition.objects.get(email_message=self.email_message)
        except ProtoProposition.DoesNotExist:
            raise AssertionError(u'proto proposition has not been created')

        # email with account details has been sent
        self.assertEqual(mock_send_email_message.mock_calls[0][2]['subject'], u'Dein Beitrag ist angekommen')
        self.assertEqual(mock_send_email_message.mock_calls[0][2]['from_email'], u'noreply@antraege.rotefabrik.de')
        self.assertListEqual(mock_send_email_message.mock_calls[0][2]['to'], [u'drechsler1840@spd.de'])

        expected_api_url = u'/api/v1/propositions/proto/{}'.format(proto_proposition.pk)

        # html
        self.assertIn(expected_api_url, mock_send_email_message.mock_calls[0][2]['html'])
        self.assertIn(user_account.user.username, mock_send_email_message.mock_calls[0][2]['html'])
        self.assertIn(expected_password, mock_send_email_message.mock_calls[0][2]['html'])

        # text
        self.assertIn(expected_api_url, mock_send_email_message.mock_calls[0][2]['html'])
        self.assertIn(user_account.user.username, mock_send_email_message.mock_calls[0][2]['text'])
        self.assertIn(expected_password, mock_send_email_message.mock_calls[0][2]['text'])
