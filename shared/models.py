from django.contrib.auth.models import User
from django.contrib.gis.db import models


class DataUpdate(models.Model):
    """A generic status update."""

    agent = models.ForeignKey(User)
    timestamp = models.DateTimeField()

    status = models.CharField(max_length=16)
    previous_status = models.CharField(max_length=16, null=True)
