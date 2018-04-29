from django.contrib.gis.db import models


class FileReference(models.Model):
    file_name = models.CharField(max_length=1024)
    path = models.TextField()
    mime_type = models.CharField(max_length=128)
    storage_engine = models.CharField(max_length=32)

    status_changes = models.ManyToManyField('shared.DataUpdate')