from django.contrib.auth.models import User
from django.contrib.gis.db import models


class UserAccount(models.Model):
    """Additional account information for a given Django user."""
    user = models.OneToOneField(User)
