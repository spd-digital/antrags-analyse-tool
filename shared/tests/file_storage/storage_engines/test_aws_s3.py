from django.test import TestCase
from django.test.utils import override_settings
from mock import MagicMock, patch
from shared.constants import DATA_UPDATE_STATUS_CREATED
from shared.file_storage.storage_engines.aws_s3 import AWSS3StorageEngine, get_s3_configuration, \
    AWSS3BucketConfigurationNotFoundError
from shared.file_storage.storage_engines.exceptions import FilenameMissingExtensionError
from shared.model_factories import UserFactory


class TestAWSS3StorageEngine(TestCase):

    def setUp(self):
        self.agent = UserFactory()

    def test_put_file_path_has_no_extension(self):
        test_destination_path = u'some/directory/document'
        with self.assertRaises(FilenameMissingExtensionError):
            AWSS3StorageEngine().put(test_destination_path, MagicMock())

    @override_settings(CDN_HOST=u'test.cdn.host')
    @patch('shared.file_storage.storage_engines.aws_s3.AWSS3StorageEngine.get_s3_client')
    @patch('shared.file_storage.storage_engines.aws_s3.AWSS3StorageEngine._generate_file_name')
    def test_put(self, mock_generate_file_name, mock_get_s3_client):
        mock_generate_file_name.return_value = u'ABC123.pdf'

        mock_client = MagicMock()
        mock_get_s3_client.return_value = mock_client

        mock_source_file = MagicMock()

        test_destination_path = u'some/directory/document.pdf'
        file_reference = AWSS3StorageEngine().put(
            test_destination_path, mock_source_file, mime_type=u'application/pdf', bucket_name=u'test.cdn.host',
            agent=self.agent)

        self.assertEqual(mock_get_s3_client.mock_calls[0][1][0], u'test.cdn.host')
        self.assertDictEqual(mock_get_s3_client.mock_calls[1][2], {
            'Body': mock_source_file,
            'Bucket': u'test.cdn.host',
            'Key': u'some/directory/ABC123.pdf',
            'Metadata': {'mime_type': u'application/pdf'}
        })
        self.assertDictEqual(mock_get_s3_client.mock_calls[2][2], {
            'ACL': u'public-read',
            'Bucket': u'test.cdn.host',
            'Key': u'some/directory/ABC123.pdf',
        })

        self.assertEqual(file_reference.file_name, u'document.pdf')
        self.assertEqual(file_reference.path, u'test.cdn.host/some/directory/ABC123.pdf')
        self.assertEqual(file_reference.mime_type, u'application/pdf')
        self.assertEqual(file_reference.storage_engine, u'aws_s3')
        self.assertEqual(file_reference.status_changes.count(), 1)
        self.assertEqual(file_reference.status_changes.get().agent, self.agent)
        self.assertEqual(file_reference.status_changes.get().status, DATA_UPDATE_STATUS_CREATED)

    @patch('shared.file_storage.storage_engines.aws_s3.AWSS3StorageEngine._download_file')
    @patch('shared.file_storage.storage_engines.aws_s3.AWSS3StorageEngine.get_s3_client')
    def test_get(self, mock_get_s3_client, mock_download_file):
        mock_s3_client = MagicMock()
        mock_get_s3_client.return_value = mock_s3_client
        test_bucket_name = u'test.bucket.de'
        test_key = U'/some/directory/document.pdf'
        test_aws_settings = {
            's3': {
                'buckets': {
                    'default': {
                        'name': test_bucket_name
                    }
                }
            }
        }

        with override_settings(AWS=test_aws_settings):
            AWSS3StorageEngine().get(test_key)

        mock_get_s3_client.assert_called_with(test_bucket_name)
        mock_download_file.assert_called_with(mock_s3_client, test_bucket_name, test_key)


class TestGetS3Configuration(TestCase):

    def setUp(self):
        self.test_bucket_name = u'test.bucket.de'
        self.test_bucket_settings1 = { 'name': self.test_bucket_name, 'test': 1 }
        self.test_bucket_settings2 = { 'name': u'some_other_bucket_name', 'test': 2 }
        self.test_aws_settings = {
            's3': {
                'buckets': {
                    'default': self.test_bucket_settings1,
                    'other_bucket': self.test_bucket_settings2
                }
            }
        }

    def test_get_s3_configuration_found(self):
        with override_settings(AWS=self.test_aws_settings):
            bucket_settings = get_s3_configuration(self.test_bucket_name)
        self.assertDictEqual(bucket_settings, self.test_bucket_settings1)

    def test_get_s3_configuration_not_found(self):
        with self.assertRaises(AWSS3BucketConfigurationNotFoundError):
            with override_settings(AWS=self.test_aws_settings):
                get_s3_configuration(u'this.is.not.the.bucket.you.are.looking.for')
