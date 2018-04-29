from shared.email.wrapper import EmailWrapper


class PropositionConfirmationEmail(EmailWrapper):
    source = u'propositions/confirmation/confirmation'
    subject = u'Dein Beitrag ist angekommen'


class PropositionConfirmationAndAccountEmail(EmailWrapper):
    source = u'propositions/confirmation_and_account/confirmation_and_account'
    subject = u'Dein Beitrag ist angekommen'
