import json

import os
from unittest import TestCase

from django.conf import settings
from django.test import RequestFactory
from django.urls import reverse
from propositions.api.v1.views import PropositionMailbox, ProtoPropositionListView
from propositions.model_factories import ProtoPropositionFactory


class TestPropositionMailbox(TestCase):

    def setUp(self):
        with open(os.path.join(settings.BASE_DIR, 'propositions/test/test_data/test_email.json'), 'r') as f:
            self.test_data = json.loads(f.read())

    def test_incoming_mail(self):
        request = RequestFactory().post(reverse('api:v1:propositions:mailbox'), data=self.test_data)
        view = PropositionMailbox.as_view()
        response = view(request)


class TestProtoPropositionListView(TestCase):

    def setUp(self):
        self.proto_proposition = ProtoPropositionFactory()

    def test_get(self):
        request = RequestFactory().get(reverse('api:v1:propositions:proto_propositions'))
        view = ProtoPropositionListView.as_view()
        response = view(request)

        response.render()

        expected_response = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "email_message": {
                        "emailattachment_set": [
                            {
                                "file_reference": {
                                    "file_name": "Antragsdatei.pdf",
                                    "id": 2,
                                    "mime_type": "application/pdf",
                                    "path": "antraege-uploads/antraege/163655/3975605767.pdf",
                                    "storage_engine": "aws_s3"
                                },
                                "id": 1
                            }
                        ],
                        "html": "<p>hier ist ein Text,<br/>wie spannend!</p>",
                        "id": 1,
                        "recipients": [
                            {
                                "address": "info@antragstest.de",
                                "id": 2,
                                "name": "Info"
                            }
                        ],
                        "sender": {
                            "address": "drechsler1840@spd.de",
                            "id": 1,
                            "name": "August Bebel"
                        },
                        "text": "hier ist ein Text, wie spannend!",
                        "raw_email_content": {
                            "file_name": "Antragsdatei.pdf",
                            "id": 1,
                            "mime_type": "application/pdf",
                            "path": "antraege-uploads/antraege/163655/3975605767.pdf",
                            "storage_engine": "aws_s3"
                        }
                    },
                    "id": 1
                }
            ]
        }

        self.assertDictEqual(json.loads(response.content), expected_response)
