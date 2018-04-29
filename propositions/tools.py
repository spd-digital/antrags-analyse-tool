from accounts.tools import get_contact_email_from_user_account
from propositions.emails.proposition_confirmation import PropositionConfirmationEmail, \
    PropositionConfirmationAndAccountEmail
from propositions.models import ProtoProposition


def create_proto_proposition_from_email_message(email_message):
    proto_proposition = ProtoProposition(email_message=email_message)
    proto_proposition.save()
    return proto_proposition


def confirm_proposition_submission(user_account, proto_proposition, password=None):
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
