import sys

import arrow
from django.conf import settings
from shared.constants import MIME_TYPE_MAPPING
from shared.file_storage.storage_engines.exceptions import FilenameMissingExtensionError
from shared.file_storage.storage_engines.local_fs import LocalFSStorageEngine
from shared.tools import generate_random_string, get_or_create_system_user

sys.path.insert(0, settings.BASE_DIR)

from shared.file_storage.storage_engines.aws_s3 import AWSS3StorageEngine

STORAGE_ENGINES = {
    'aws_s3': AWSS3StorageEngine,
    'local_fs': LocalFSStorageEngine
}

class StorageEngineNotSupportedError(AssertionError):
    pass


def put_file(*args, **kwargs):
    """Persist a file to the active storage engine."""
    storage_engine_key = settings.STORAGE_ENGINE
    if storage_engine_key not in STORAGE_ENGINES:
        raise StorageEngineNotSupportedError(u'the storage engine {} is not supported'.format(storage_engine_key))
    return STORAGE_ENGINES[settings.STORAGE_ENGINE]().put(*args, **kwargs)


def get_file(*args, **kwargs):
    """Get a file from the active storage engine."""
    storage_engine_key = settings.STORAGE_ENGINE
    if storage_engine_key not in STORAGE_ENGINES:
        raise StorageEngineNotSupportedError(u'the storage engine {} is not supported'.format(storage_engine_key))
    return STORAGE_ENGINES[settings.STORAGE_ENGINE]().get(*args, **kwargs)


def generate_file_name(file_extension=None):
    """Generate a file name.

    Args:
        file_extension (unicode): optional file extension

    Returns (unicode): a generate file name

    """
    file_name = generate_random_string(length=16)
    return u'{}.{}'.format(file_name, file_extension) if file_extension else file_name


def get_mime_type_for_file_extension(file_extension):
    """returns a mime type for a file extension for limited set of mapped options

    Args:
        file_extension (unicode): a file extension, ex: pdf

    Returns (unicode): a mime type string, ex: application/pdf

    """
    return MIME_TYPE_MAPPING[file_extension] if file_extension in MIME_TYPE_MAPPING else None


def assert_file_name_has_extension(file_name):
    """checks if a file name contains a file extension.

    Args:
        file_name (string): a file name, ex: hello_world.pdf

    Returns (boolean): True if the file name contains a file extension, else False

    """
    if len(file_name.split('.')) < 2:
        raise FilenameMissingExtensionError(file_name)
