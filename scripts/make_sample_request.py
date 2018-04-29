import json

import os
import sys

import requests
from django.conf import settings


def make_sample_request():
    with open(os.path.join(settings.BASE_DIR, 'propositions/test/test_data/test_email.json'), 'r') as f:
        json_source = json.loads(f.read())
    requests.post(u'http://127.0.0.1:8000/api/v1/propositions/mailbox/', data=json_source)


if __name__ == '__main__':
    import django
    django.setup()
    make_sample_request()
