from accounts.models import UserAccount
from django.contrib.auth.models import User
from django.db import transaction
from shared.tools import generate_random_string


class AccountDoesNotExistError(AssertionError):
    pass


class CannotCreateAccountForExistingUserError(AssertionError):
    pass


def get_account_by_email(email_address_string):
    try:
        return UserAccount.objects.get(user__email=email_address_string)
    except UserAccount.DoesNotExist:
        raise AccountDoesNotExistError(
            u'no user account found for email {}'.format(email_address_string))


@transaction.atomic
def create_account_from_email_address(email_address):
    try:
        user = User.objects.get(email=email_address.address)
        raise CannotCreateAccountForExistingUserError(
            u'cannot create user account: user with email {} already exists: {} [{}]'.format(
                email_address.address, user.username, user.pk))
    except User.DoesNotExist:
        username = generate_username()
        password = generate_password()
        user = User.objects.create_user(username=username, email=email_address.address, password=password)

    user_account = UserAccount(user=user)
    user_account.save()

    return user_account, password


def generate_username():
    return generate_random_string()


def generate_password():
    return generate_random_string()


def get_contact_email_from_user_account(user_account):
    return user_account.user.email
