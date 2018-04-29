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
        MandrillTransmissionWrapper(self.json_source)
