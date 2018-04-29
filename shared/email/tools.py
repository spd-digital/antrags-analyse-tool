from accounts.tools import AccountDoesNotExistError, create_account_from_email_address
from accounts.tools import get_account_by_email
from django.db import transaction
from shared.email.models import EmailAddress


def get_or_create_email_address(email_address, email_name=None):
    try:
        return EmailAddress.objects.get(address=email_address)
    except EmailAddress.DoesNotExist:
        return create_email_address(email_address, email_name=email_name)


@transaction.atomic
def create_email_address(email_address, email_name=None):
    email_address = EmailAddress(address=email_address, name=email_name)
    email_address.save()
    return email_address


@transaction.atomic
def get_or_create_user_account_for_email_message(email_message):
    try:
        account = get_account_by_email(email_message.sender.address)
        return account, None
    except AccountDoesNotExistError:
        return create_account_from_email_address(email_message.sender)