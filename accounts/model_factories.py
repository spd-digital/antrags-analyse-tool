import factory
from accounts.models import UserAccount
from shared.model_factories import UserFactory


class UserAccountFactory(factory.DjangoModelFactory):
    """Factory for a generic user account."""
    class Meta:
        model = UserAccount

    user = factory.SubFactory(UserFactory)
