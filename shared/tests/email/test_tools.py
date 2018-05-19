from accounts.model_factories import UserAccountFactory
from accounts.tools import AccountDoesNotExistError
from django.test import TestCase
from django.test.utils import tag
from mock import patch, MagicMock
from model_mommy import mommy
from shared.email.model_factories import EmailAddressFactory, EmailMessageFactory
from shared.email.models import EmailAddress
from shared.email.tools import get_or_create_email_address, create_email_address, \
    get_or_create_user_account_for_email_message


class TestGetOrCreateEmailAddress(TestCase):

    def setUp(self):
        self.email_address = EmailAddressFactory()

    @tag('integration')
    def test_get_or_create_email_address_get(self):
        email_address = get_or_create_email_address(self.email_address.address)
        self.assertEqual(email_address, self.email_address)

    @tag('integration')
    def test_get_or_create_email_address_create(self):
        test_address = u'Wilhelm Liebknecht'
        test_name = u'wilhelm@adav.de'
        email_address = get_or_create_email_address(test_address, email_name=test_name)
        self.assertEqual(email_address.name, test_name)
        self.assertEqual(email_address.address, test_address)


class TestCreateEmailAddress(TestCase):

    @tag('integration')
    def test_create_email_address(self):
        test_address = u'karl.liebknecht@wer-braucht-bernstein.de'
        test_name = u'Karl Kautsky'
        email_address = create_email_address(test_address, email_name=test_name)
        self.assertEqual(email_address.address, test_address)
        self.assertEqual(email_address.name, test_name)


class TestGetOrCreateUserAccountForEmailMessage(TestCase):

    def setUp(self):
        self.user_account = UserAccountFactory()
        self.email_address = mommy.make(EmailAddress, address=self.user_account.user.email, name=u'Rosa Luxemburg')
        self.email_message = EmailMessageFactory(sender=self.email_address)

    @patch('shared.email.tools.get_account_by_email')
    def test_get_or_create_user_account_for_email_message_success_get(self, mock_get_account_by_email):
        mock_email_message = MagicMock()
        mock_account = MagicMock()
        mock_get_account_by_email.return_value = mock_account
        user_account, password = get_or_create_user_account_for_email_message(mock_email_message)
        self.assertEqual(user_account, mock_account)
        self.assertIsNone(password)

    @patch('shared.email.tools.create_account_from_email_address')
    @patch('shared.email.tools.get_account_by_email')
    def test_get_or_create_user_account_for_email_message_success_create(
            self, mock_get_account_by_email, mock_create_account_from_email_address):
        mock_sender = MagicMock()
        mock_email_message = MagicMock(sender=mock_sender)
        mock_get_account_by_email.side_effect = AccountDoesNotExistError()
        get_or_create_user_account_for_email_message(mock_email_message)
        mock_create_account_from_email_address.assert_called_with(mock_sender)
