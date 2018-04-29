from django.contrib.gis.db import models


class EmailAddress(models.Model):
    name = models.CharField(max_length=255, null=True)
    address = models.EmailField(unique=True)


class EmailMessage(models.Model):
    sender = models.ForeignKey('email.EmailAddress', related_name=u'sender')
    recipients = models.ManyToManyField('email.EmailAddress', related_name=u'recipients')

    text = models.TextField()
    html = models.TextField()

    raw_email_content = models.ForeignKey('file_storage.FileReference', null=True)


class EmailAttachment(models.Model):
    email_message = models.ForeignKey('email.EmailMessage')
    file_reference = models.ForeignKey('file_storage.FileReference')
