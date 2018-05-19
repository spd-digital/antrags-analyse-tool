import json

import os
from django.conf import settings
from django.test import TestCase
from shared.mandrill.wrappers.transmission import MandrillTransmissionWrapper


class TestMandrillEvents(TestCase):

    def setUp(self):
        with open(os.path.join(settings.BASE_DIR, 'propositions/test/test_data/test_email.json'), 'r') as f:
            self.json_source = json.loads(f.read())

    def test_mandrill_events(self):
        actual_wrapper = MandrillTransmissionWrapper(self.json_source)

        self.assertEqual(len(actual_wrapper.events), 1)

        self.assertEqual(actual_wrapper.events[0].email, u'antrag@antraege.rotefabrik.de')

        self.assertEqual(len(actual_wrapper.events[0].attachments), 1)

        self.assertEqual(actual_wrapper.events[0].attachments[0].file_name, u'180409_Leitantrag.pdf')
