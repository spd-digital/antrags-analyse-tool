from django.contrib.gis.db import models


class FileReference(models.Model):
    """Database representation of a file stored via a given storage engine."""
    file_name = models.CharField(max_length=1024)
    path = models.TextField()
    mime_type = models.CharField(max_length=128)
    storage_engine = models.CharField(max_length=32)

    status_changes = models.ManyToManyField('shared.DataUpdate')