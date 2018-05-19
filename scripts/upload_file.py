"""Script for uploading a file to storage."""

import sys

import django
django.setup()

from shared.file_storage.tools import put_file


def upload_file(destination_path, source_file):
    with open(source_file, 'rb') as f:
        print put_file(destination_path, f)


if __name__ == '__main__':
    upload_file(sys.argv[1], sys.argv[2])
