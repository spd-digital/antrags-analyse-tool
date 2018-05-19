import errno
import shutil

from io import BytesIO

import os
from django.conf import settings

from shared.file_storage.storage_engines.base import StorageEngine


class LocalFSStorageEngine(StorageEngine):
    """
    Implementation for local file system storage.
    WARNING: use only in local development due to lack of limitations on host file system access.
    """
    storage_engine = 'local_fs'

    def _put(self, destination_path, source_file, *args, **kwargs):
        path = os.path.dirname(destination_path)
        file_name = os.path.basename(destination_path)

        from shared.file_storage.tools import assert_file_name_has_extension
        assert_file_name_has_extension(file_name)

        file_extension = file_name.split('.')[-1]
        generated_file_name = self._generate_file_name(file_extension=file_extension)

        generated_destination_path = os.path.join(settings.LOCAL_STORAGE_PATH, path, generated_file_name)

        self._ensure_directory_path_exists(os.path.dirname(generated_destination_path))

        with open(generated_destination_path, 'wb') as f:
            source_file.seek(0)
            shutil.copyfileobj(source_file, f)

        return file_name, generated_destination_path

    def _ensure_directory_path_exists(self, directory_path):
        try:
            os.makedirs(directory_path)
        except OSError as e:
            print e
            if e.errno != errno.EEXIST:
                raise

    def get(self, path, *args, **kwargs):
        with open(path, 'rb') as f:
            bytes_buffer = BytesIO(f.read())
            return bytes_buffer
