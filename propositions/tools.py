from accounts.tools import get_contact_email_from_user_account
from propositions.emails.proposition_confirmation import PropositionConfirmationEmail, \
    PropositionConfirmationAndAccountEmail
from propositions.models import ProtoProposition


def create_proto_proposition_from_email_message(email_message):
    """Persist the information in an email message to a proto proposition.

    Args:
        email_message: database representation of the content of an email.

    Returns (ProtoProposition): database representation of the unvetted data collection.

    """
    proto_proposition = ProtoProposition(email_message=email_message)
    proto_proposition.save()
    return proto_proposition


def confirm_proposition_submission(user_account, proto_proposition, password=None):
    """Inform the user having submitted a proposition that their submission has been received successfully.

    Args:
        user_account (UserAccount): the user account of the submitting user.
        proto_proposition (ProtoProposition): where the data has been preliminarily stored.
        password (unicode): the submitting user's password, in case this is the first action for this email.

    Returns:

    """
    contact_email = get_contact_email_from_user_account(user_account)
    if password is None:
        PropositionConfirmationEmail(
            user_account=user_account,
            proto_proposition=proto_proposition)\
            .send(recipients=[contact_email])
    else:
        PropositionConfirmationAndAccountEmail(
            user_account=user_account,
            proto_proposition=proto_proposition,
            password=password)\
            .send(recipients=[contact_email])
