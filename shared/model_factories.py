"""Factories for generic shared models."""

import arrow
import factory
from django.contrib.auth.models import User
from shared.models import DataUpdate


class UserFactory(factory.DjangoModelFactory):
    """Factory for a standard Django user."""

    class Meta:
        model = User

    username = u'XSJEGH123'
    first_name = u'Karl'
    last_name = u'Liebknecht'
    email = u'liebknecht@wiedervatersodersohn.de'
    is_staff = False
    is_active = True
    date_joined = arrow.get(2018, 4, 28).date()


class DataUpdateFactory(factory.DjangoModelFactory):
    """Factory for a generic status update."""

    class Meta:
        model = DataUpdate

    agent = factory.SubFactory(UserFactory)
    timestamp = arrow.get(2018, 4, 28, 13, 30, 5).datetime

    status = u'created'
    previous_status = None
