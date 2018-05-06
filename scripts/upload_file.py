"""Script for uploading a file to storage."""

import django
import sys

from shared.file_storage.tools import put_file


def upload_file(destination_path, source_file):
    with open(source_file, 'rb') as f:
        print put_file(destination_path, f)


if __name__ == '__main__':
    django.setup()
    upload_file(sys.argv[1], sys.argv[2])
