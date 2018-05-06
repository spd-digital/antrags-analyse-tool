"""Script for downloading a file from storage."""

import django
import sys

from shared.file_storage.tools import get_file


def upload_file(source_path):
    get_file(source_path)


if __name__ == '__main__':
    django.setup()
    upload_file(sys.argv[1])
