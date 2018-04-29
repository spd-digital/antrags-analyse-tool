from django.contrib.gis.db import models


class ProtoProposition(models.Model):
    email_message = models.ForeignKey('email.EmailMessage')
