# coding=utf-8
from django.test import TestCase
from django.test.utils import override_settings, tag
from mock import patch
from mock.mock import MagicMock
from nose_parameterized import parameterized
from shared.file_storage import tools
from shared.file_storage.storage_engines.exceptions import FilenameMissingExtensionError
from shared.file_storage.tools import StorageEngineNotSupportedError, generate_file_name, \
    get_mime_type_for_file_extension, assert_file_name_has_extension


class TestPutFile(TestCase):

    @tag('unit')
    def test_put_file_engine_supported(self):
        test_arg = MagicMock()
        test_kwarg = MagicMock()

        mock_storage_engine = MagicMock()
        tools.STORAGE_ENGINES = {u'aws_s3': mock_storage_engine}

        with override_settings(STORAGE_ENGINE=u'aws_s3'):
            tools.put_file(test_arg, test=test_kwarg)

        mock_storage_engine.return_value.put.assert_called_with(test_arg, test=test_kwarg)

    @tag('unit')
    def test_put_file_engine_not_supported(self):
        test_arg = MagicMock()
        test_kwarg = MagicMock()

        mock_storage_engine = MagicMock()
        tools.STORAGE_ENGINES = {u'aws_s3': mock_storage_engine}

        unsupported_storage_engine_key = u'unsupported_storage_engine'

        with self.assertRaises(StorageEngineNotSupportedError) as e:
            with override_settings(STORAGE_ENGINE=unsupported_storage_engine_key):
                tools.put_file(test_arg, test=test_kwarg)
        self.assertEqual(e.exception.message, u'the storage engine {} is not supported'
                         .format(unsupported_storage_engine_key))


class TestGetFile(TestCase):

    @tag('unit')
    def test_get_file_engine_supported(self):
        test_arg = MagicMock()
        test_kwarg = MagicMock()

        mock_storage_engine = MagicMock()
        tools.STORAGE_ENGINES = {u'aws_s3': mock_storage_engine}

        with override_settings(STORAGE_ENGINE=u'aws_s3'):
            tools.get_file(test_arg, test=test_kwarg)

        mock_storage_engine.return_value.get.assert_called_with(test_arg, test=test_kwarg)

    @tag('unit')
    def test_get_file_engine_not_supported(self):
        test_arg = MagicMock()
        test_kwarg = MagicMock()

        mock_storage_engine = MagicMock()
        tools.STORAGE_ENGINES = {u'aws_s3': mock_storage_engine}

        unsupported_storage_engine_key = u'unsupported_storage_engine'

        with self.assertRaises(StorageEngineNotSupportedError) as e:
            with override_settings(STORAGE_ENGINE=unsupported_storage_engine_key):
                tools.get_file(test_arg, test=test_kwarg)
        self.assertEqual(e.exception.message, u'the storage engine {} is not supported'
                         .format(unsupported_storage_engine_key))


class TestGenerateFileName(TestCase):

    @patch('shared.file_storage.tools.generate_random_string')
    def test_generate_file_name_without_file_extension(self, mock_generate_random_string):
        mock_generate_random_string.return_value = u'ABC123'
        generated_file_name = generate_file_name(file_extension=None)
        self.assertEqual(generated_file_name, u'ABC123')

    @patch('shared.file_storage.tools.generate_random_string')
    def test_generate_file_name_with_file_extension(self, mock_generate_random_string):
        mock_generate_random_string.return_value = u'ABC123'
        generated_file_name = generate_file_name(file_extension=u'pdf')
        self.assertEqual(generated_file_name, u'ABC123.pdf')


class TestGetMimeTypeForFileExtension(TestCase):

    @parameterized.expand([
        ('doc', u'application/msword'),
        ('docx', u'application/vnd.openxmlformats-officedocument.wordprocessingml.document'),
        ('html', u'text/html'),
        ('odt', u'application/vnd.oasis.opendocument.text'),
        ('pdf', u'application/pdf'),
        ('txt', u'text/plain')
    ])
    def test_get_mime_type_for_file_extension(self, test_file_extension, expected_mime_type):
        self.assertEqual(get_mime_type_for_file_extension(test_file_extension), expected_mime_type)


class TestAssertFileNameHasExtension(TestCase):

    @parameterized.expand([
        ('myfile', False),
        ('myfile.txt', True),
        ('myfile.backup.txt', True)
    ])
    def test_assert_file_name_has_extension_true(self, test_file_name, test_file_name_has_extension):
        if test_file_name_has_extension:
            try:
                assert_file_name_has_extension(test_file_name)
            except FilenameMissingExtensionError:
                raise AssertionError(
                    u'expected file name to be recognized as having a file extension: {}'.format(test_file_name))
        else:
            with self.assertRaises(FilenameMissingExtensionError):
                assert_file_name_has_extension(test_file_name)
