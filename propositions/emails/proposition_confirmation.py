from shared.email.wrapper import EmailWrapper


class PropositionConfirmationEmail(EmailWrapper):
    """An email confirming a proposition has been submitted."""
    source = u'propositions/confirmation/confirmation'
    subject = u'Dein Beitrag ist angekommen'


class PropositionConfirmationAndAccountEmail(EmailWrapper):
    """
    An email confirming a proposition has been submitted,
    which also includes information about the user account of the user having submitted the proposition.
    """
    source = u'propositions/confirmation_and_account/confirmation_and_account'
    subject = u'Dein Beitrag ist angekommen'
