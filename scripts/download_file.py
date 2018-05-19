"""Script for downloading a file from storage."""
import sys
import shutil

import django
django.setup()

from shared.file_storage.tools import get_file


def download_file(source_path, destination_path):
    source_file = get_file(source_path)
    with open(destination_path, 'wb') as f:
        source_file.seek(0)
        shutil.copyfileobj(source_file, f)


if __name__ == '__main__':
    django.setup()
    download_file(sys.argv[1], sys.argv[2])
