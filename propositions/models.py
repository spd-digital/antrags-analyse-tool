from django.contrib.gis.db import models


class ProtoProposition(models.Model):
    """An unvetted data collection from which a proposition for publication can be generated."""
    email_message = models.ForeignKey('email.EmailMessage')
