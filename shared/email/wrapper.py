import os

from django.conf import settings
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string


class CannotSendEmailsOutsideProductionEnvironmentError(AssertionError):
    def __init__(self):
        super(CannotSendEmailsOutsideProductionEnvironmentError, self).__init__(
            u'non-production environment detected. Refusing to send any emails')


class EmailWrapper(object):
    source = None
    subject = None

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def send(self, recipients=None, cc=None, bcc=None):
        sender = self.get_from() or settings.DEFAULT_EMAIL_SENDER

        recipients = recipients or self.kwargs.get('recipients') or self.get_to()
        cc = cc or self.kwargs.get('cc') or self.get_cc()
        bcc = bcc or self.kwargs.get('bcc') or self.get_bcc()

        subject = self.subject or self.get_subject()

        text = self.get_text()
        html = self.get_html()

        attachments = self.get_attachments()
        headers = self.get_headers()
        alternatives = self.get_alternatives()
        reply_to = self.get_reply_to()
        connection = self.get_connection()

        fail_silently = self.get_fail_silently()

        self.send_email_message(
            subject=subject, text=text, from_email=sender, to=recipients, cc=cc, bcc=bcc, attachments=attachments,
            connection=connection, headers=headers, alternatives=alternatives, reply_to=reply_to, html=html,
            fail_silently=fail_silently)

    def send_email_message(
            self, subject=None, text=None, html=None, from_email=None, to=None, cc=None, bcc=None, attachments=None,
            connection=None, headers=None, alternatives=None, reply_to=None, fail_silently=False):

        if not settings.PRODUCTION:
            raise CannotSendEmailsOutsideProductionEnvironmentError()

        message = EmailMultiAlternatives(
            subject=subject,

            body=text,

            from_email=from_email,
            to=to,
            cc=cc,
            bcc=bcc,

            attachments=attachments,

            connection=connection,

            headers=headers,
            alternatives=alternatives,
            reply_to=reply_to)

        if html:
            message.attach_alternative(html, "text/html")

        message.send(fail_silently=fail_silently)

    def get_from(self):
        return None

    def get_to(self):
        raise NotImplementedError()

    def get_cc(self):
        return None

    def get_bcc(self):
        return None

    def get_subject(self):
        return None

    def get_text(self):
        return self.render_template(extension='txt')

    def get_html(self):
        return self.render_template(extension='html')

    def get_headers(self):
        return None

    def get_attachments(self):
        return None

    def get_alternatives(self):
        return None

    def get_fail_silently(self):
        return False

    def get_reply_to(self):
        return None

    def get_connection(self):
        return None

    def render_template(self, extension='txt'):
        template_path = self.get_template_path(extension)
        context = self.get_context()
        return render_to_string(template_path, context)

    def get_template_path(self, extension):
        return u'emails/{}.{}'.format(self.source, extension)

    def get_context(self):
        generic_context = self.get_generic_context()
        generic_context.update(self.kwargs)
        return generic_context

    def get_generic_context(self):
        return {
            'host': settings.SITE_HOST
        }
