import factory
from shared.email.models import EmailMessage, EmailAddress, EmailAttachment
from shared.file_storage.model_factories import FileReferenceFactory


class EmailAttachmentFactory(factory.DjangoModelFactory):
    class Meta:
        model = EmailAttachment

    email_message = factory.SubFactory('shared.email.models_factories.EmailMessageFactory')
    file_reference = factory.SubFactory('shared.file_storage.model_factories.FileReferenceFactory')


class EmailAddressSenderFactory(factory.DjangoModelFactory):
    class Meta:
        model = EmailAddress

    name = u'August Bebel'
    address = u'drechsler1840@spd.de'


class EmailAddressRecipientFactory(factory.DjangoModelFactory):
    class Meta:
        model = EmailAddress

    name = u'Info'
    address = u'info@antragstest.de'


class EmailMessageFactory(factory.DjangoModelFactory):
    class Meta:
        model = EmailMessage

    text = u'hier ist ein Text, wie spannend!'
    html = u'<p>hier ist ein Text,<br/>wie spannend!</p>'

    sender = factory.SubFactory('shared.email.model_factories.EmailAddressSenderFactory')

    raw_email_content = factory.SubFactory('shared.file_storage.model_factories.FileReferenceFactory')

    @factory.post_generation
    def recipients(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for recipient in extracted:
                self.recipients.add(recipient)
        else:
            recipient = EmailAddressRecipientFactory()
            self.recipients.add(recipient)

    attachments = factory.RelatedFactory(EmailAttachmentFactory, 'email_message')
