import boto3
import os

from django.conf import settings
from shared.file_storage.storage_engines.base import StorageEngine
from shared.file_storage.storage_engines.exceptions import FilenameMissingExtensionError


ACL_PRIVATE = u'private'
ACL_PUBLIC_READ = u'public-read'
ACL_PUBLIC_READ_WRITE = u'public-read-write'
ACL_AUTHENTICATED_READ = u'authenticated-read'
ACL_AWS_EXEC_READ = u'aws-exec-read'
ACL_BUCKET_OWNER_READ = u'bucket-owner-read'
ACL_BUCKET_OWNER_FULL_CONTROL = u'bucket-owner-full-control'


class AWSS3BucketConfigurationNotFoundError(AssertionError):
    def __init__(self, bucket_name):
        message = u'no configuration found for AWS S3 bucket {}'.format(bucket_name)
        super(AWSS3BucketConfigurationNotFoundError, self).__init__(message)


class AWSS3StorageEngine(StorageEngine):
    storage_engine = 'aws_s3'

    def _put(self, destination_path, source_file, *args, **kwargs):
        bucket_name = kwargs.get('bucket_name', settings.AWS['s3']['buckets']['default']['name'])
        file_name = os.path.basename(destination_path)

        if len(file_name.split('.')) < 2:
            raise FilenameMissingExtensionError(file_name)
        file_extension = file_name.split('.')[-1]
        from shared.file_storage.tools import generate_file_name
        generated_file_name = generate_file_name(file_extension=file_extension)

        key = os.path.join(os.path.dirname(destination_path), generated_file_name)

        client = self.get_s3_client(bucket_name)
        client.put_object(Body=source_file, Bucket=bucket_name, Key=key)
        client.put_object_acl(ACL=ACL_PUBLIC_READ, Bucket=bucket_name, Key=key)

        return file_name, os.path.join(settings.CDN_HOST, key)

    def get(self, source_path, *args, **kwargs):
        bucket_name = source_path.split(os.sep)[0]
        key = os.sep.join(source_path.split(os.sep)[1:])

        client = self.get_s3_client(bucket_name)

        with open(os.path.join(settings.BASE_DIR, '.tmp', key), 'wb') as data:
            client.download_fileobj(bucket_name, key, data)

    def get_s3_client(self, bucket_name):
        s3_bucket_configuration = get_s3_configuration(bucket_name)
        return boto3.client('s3', aws_access_key_id=s3_bucket_configuration.get('access_key'),
                     aws_secret_access_key=s3_bucket_configuration.get('secret_access_key'))


def get_s3_configuration(bucket_name):
    for bucket_setting in settings.AWS['s3']['buckets'].values():
        if bucket_setting.get('name') == bucket_name:
            return bucket_setting
    raise AWSS3BucketConfigurationNotFoundError(bucket_name)
