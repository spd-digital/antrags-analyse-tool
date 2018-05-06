from django.contrib.gis.db import models


class EmailAddress(models.Model):
    """An email address, including a display name."""
    name = models.CharField(max_length=255, null=True)
    address = models.EmailField(unique=True)


class EmailMessage(models.Model):
    """An email message with both text and HTML content."""
    sender = models.ForeignKey('email.EmailAddress', related_name=u'sender')
    recipients = models.ManyToManyField('email.EmailAddress', related_name=u'recipients')

    text = models.TextField()
    html = models.TextField()

    raw_email_content = models.ForeignKey('file_storage.FileReference', null=True)


class EmailAttachment(models.Model):
    """A file attachment associated with an email message."""
    email_message = models.ForeignKey('email.EmailMessage')
    file_reference = models.ForeignKey('file_storage.FileReference')
