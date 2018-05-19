import json

import os

from django.conf import settings
from django.test import RequestFactory
from django.test.testcases import TestCase
from django.urls import reverse
from mock import patch, MagicMock
from propositions.api.v1.views import PropositionMailbox, ProtoPropositionListView
from propositions.model_factories import ProtoPropositionFactory
from propositions.models import ProtoProposition
from shared.email.models import EmailAddress, EmailAttachment, EmailMessage
from shared.file_storage.models import FileReference


class TestPropositionMailbox(TestCase):

    def setUp(self):
        with open(os.path.join(settings.BASE_DIR, 'propositions/test/test_data/test_email.json'), 'r') as f:
            self.test_data = json.loads(f.read())

    @patch('propositions.api.v1.views.submit_proposition_by_emails')
    @patch('propositions.api.v1.views.persist_email_messages')
    @patch('propositions.api.v1.views.save_raw_email_message')
    def test_incoming_mail(self, mock_save_raw_email_message, mock_persist_email_messages,
                           mock_submit_proposition_by_emails):
        mock_email_messages = [MagicMock()]
        mock_persist_email_messages.return_value = mock_email_messages

        request = RequestFactory().post(reverse('api:v1:propositions:mailbox'), data=self.test_data)
        view = PropositionMailbox.as_view()
        response = view(request)

        mock_submit_proposition_by_emails.assert_called_with(mock_email_messages)


class TestProtoPropositionListView(TestCase):

    def setUp(self):
        self.proto_proposition = ProtoPropositionFactory()

    def test_get(self):
        self.maxDiff = None
        request = RequestFactory().get(reverse('api:v1:propositions:proto_propositions'))
        view = ProtoPropositionListView.as_view()
        response = view(request)

        response.render()

        expected_response = {
            u"count": 1,
            u"next": None,
            u"previous": None,
            u"results": [
                {
                    u"email_message": {
                        u"emailattachment_set": [
                            {
                                u"file_reference": {
                                    u"file_name": u"Antragsdatei.pdf",
                                    u"id": FileReference.objects.last().pk,
                                    u"mime_type": u"application/pdf",
                                    u"path": u"antraege-uploads/antraege/163655/3975605767.pdf",
                                    u"storage_engine": u"aws_s3"
                                },
                                u"id": EmailAttachment.objects.last().pk
                            }
                        ],
                        u"html": u"<p>hier ist ein Text,<br/>wie spannend!</p>",
                        u"id": EmailMessage.objects.last().pk,
                        u"recipients": [
                            {
                                u"address": u"info@antragstest.de",
                                u"id": EmailAddress.objects.get(name=u'Info').pk,
                                u"name": u"Info"
                            }
                        ],
                        u"sender": {
                            u"address": u"drechsler1840@spd.de",
                            u"id": EmailAddress.objects.get(name=u'August Bebel').pk,
                            u"name": u"August Bebel"
                        },
                        u"text": u"hier ist ein Text, wie spannend!",
                        u"raw_email_content": {
                            u"file_name": u"Antragsdatei.pdf",
                            u"id": FileReference.objects.first().pk,
                            u"mime_type": u"application/pdf",
                            u"path": u"antraege-uploads/antraege/163655/3975605767.pdf",
                            u"storage_engine": u"aws_s3"
                        }
                    },
                    u"id": ProtoProposition.objects.get().pk
                }
            ]
        }

        self.assertDictEqual(json.loads(response.content), expected_response)
