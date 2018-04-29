import factory
from propositions.models import ProtoProposition
from shared.email.model_factories import EmailMessageFactory


class ProtoPropositionFactory(factory.DjangoModelFactory):
    class Meta:
        model = ProtoProposition

    email_message = factory.SubFactory(EmailMessageFactory)
