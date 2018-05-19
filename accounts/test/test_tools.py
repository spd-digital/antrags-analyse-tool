from accounts.model_factories import UserAccountFactory
from accounts.models import UserAccount
from accounts.tools import get_account_by_email, AccountDoesNotExistError, create_account_from_email_address, \
    CannotCreateAccountForExistingUserError
from django.test import tag
from django.test.testcases import TestCase
from model_mommy import mommy
from shared.email.models import EmailAddress
from shared.model_factories import UserFactory


class TestGetAccountByEmail(TestCase):

    def setUp(self):
        self.user_account = UserAccountFactory()

    @tag('integration')
    def test_get_account_by_email_success(self):
        self.assertEqual(get_account_by_email(self.user_account.user.email), self.user_account)

    @tag('integration')
    def test_get_account_by_email_failure(self):
        with self.assertRaises(AccountDoesNotExistError):
            get_account_by_email(u'some_other_email@nowhere.com')


class TestCreateAccountFromEmailAddress(TestCase):

    def setUp(self):
        self.user = UserFactory()
        self.email_address = mommy.make(EmailAddress, name=u'Marie Musterfrau', address=self.user.email)

    @tag('integration')
    def test_create_account_from_email_address_user_exists(self):
        with self.assertRaises(CannotCreateAccountForExistingUserError):
            user_account, _ = create_account_from_email_address(self.email_address)

    @tag('integration')
    def test_create_account_from_email_address_user_does_not_exist(self):
        other_email_address = mommy.make(EmailAddress, name=u'Max Mustermann', address=u'max@mustermann.de')
        user_account, _ = create_account_from_email_address(other_email_address)
        self.assertIsInstance(user_account, UserAccount)
        self.assertNotEqual(user_account.user, self.user)
