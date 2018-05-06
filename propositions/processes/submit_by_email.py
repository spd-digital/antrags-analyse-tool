from propositions.tools import create_proto_proposition_from_email_message, confirm_proposition_submission
from shared.email.tools import get_or_create_user_account_for_email_message


def submit_proposition_by_emails(email_messages):
    """Processes multiple email messages (potentially) containing propositions.

    Args:
        email_messages (list): list of EmailMessage instances.

    Returns:

    """
    for email_message in email_messages:
        submit_proposition_by_email(email_message)


def submit_proposition_by_email(email_message):
    """Processes a single email message (potentially) containing a proposition.

    Args:
        email_message (EmailMessage): database representation of an email message.

    Returns:

    """
    user_account, password = get_or_create_user_account_for_email_message(email_message)
    proto_proposition = create_proto_proposition_from_email_message(email_message)
    confirm_proposition_submission(user_account, proto_proposition, password=password)
