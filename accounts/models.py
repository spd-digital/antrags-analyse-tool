from django.contrib.auth.models import User
from django.contrib.gis.db import models


class UserAccount(models.Model):
    user = models.OneToOneField(User)
