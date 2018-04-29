from propositions.tools import create_proto_proposition_from_email_message, confirm_proposition_submission
from shared.email.tools import get_or_create_user_account_for_email_message


def submit_proposition_by_emails(email_messages):
    for email_message in email_messages:
        submit_proposition_by_email(email_message)


def submit_proposition_by_email(email_message):
    user_account, password = get_or_create_user_account_for_email_message(email_message)
    proto_proposition = create_proto_proposition_from_email_message(email_message)
    confirm_proposition_submission(user_account, proto_proposition, password=password)
