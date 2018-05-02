from django.test import tag
from django.test.testcases import TestCase
from mock import patch, MagicMock
from propositions.tools import create_proto_proposition_from_email_message, confirm_proposition_submission
from shared.email.model_factories import EmailMessageFactory


class TestCreateProtoPropositionFromEmailMessage(TestCase):

    def setUp(self):
        self.email_message = EmailMessageFactory()

    @tag('integration')
    def test_create_proto_proposition_from_email_message(self):
        proto_proposition = create_proto_proposition_from_email_message(self.email_message)
        self.assertEqual(proto_proposition.email_message, self.email_message)


class TestConfirmPropositionSubmission(TestCase):

    @patch('propositions.tools.PropositionConfirmationAndAccountEmail')
    @patch('propositions.tools.PropositionConfirmationEmail')
    @patch('propositions.tools.get_contact_email_from_user_account')
    def test_confirm_proposition_submission_without_password(
            self, mock_get_contact_email_from_user_account, MockPropositionConfirmationEmail,
            MockPropositionConfirmationAndAccountEmail):
        test_contact_email = u'test@test.de'
        mock_get_contact_email_from_user_account.return_value = test_contact_email
        mock_user_account = MagicMock()
        mock_proto_proposition = MagicMock()

        confirm_proposition_submission(mock_user_account, mock_proto_proposition, password=None)

        MockPropositionConfirmationEmail.return_value.send.assert_called_with(recipients=[test_contact_email])
        self.assertEqual(len(MockPropositionConfirmationAndAccountEmail.mock_calls), 0)

    @patch('propositions.tools.PropositionConfirmationAndAccountEmail')
    @patch('propositions.tools.PropositionConfirmationEmail')
    @patch('propositions.tools.get_contact_email_from_user_account')
    def test_confirm_proposition_submission_with_password(
            self, mock_get_contact_email_from_user_account, MockPropositionConfirmationEmail,
            MockPropositionConfirmationAndAccountEmail):
        test_contact_email = u'test@test.de'
        mock_get_contact_email_from_user_account.return_value = test_contact_email
        mock_user_account = MagicMock()
        mock_proto_proposition = MagicMock()

        confirm_proposition_submission(mock_user_account, mock_proto_proposition, password=u'somepassword')

        MockPropositionConfirmationAndAccountEmail.return_value.send.assert_called_with(recipients=[test_contact_email])
        self.assertEqual(len(MockPropositionConfirmationEmail.mock_calls), 0)
