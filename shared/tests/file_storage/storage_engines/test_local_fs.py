from django.test.testcases import TestCase
from mock import MagicMock, patch
from shared.file_storage.storage_engines.exceptions import FilenameMissingExtensionError
from shared.file_storage.storage_engines.local_fs import LocalFSStorageEngine
from shared.model_factories import UserFactory


class TestLocalFS(TestCase):

    def setUp(self):
        self.agent = UserFactory()

    def test_put_file_path_has_no_extension(self):
        test_destination_path = u'some/directory/document'
        with self.assertRaises(FilenameMissingExtensionError):
            LocalFSStorageEngine().put(test_destination_path, MagicMock())

    @patch('shared.file_storage.storage_engines.local_fs.LocalFSStorageEngine._ensure_directory_path_exists')
    @patch('shared.file_storage.storage_engines.local_fs.shutil')
    @patch('shared.file_storage.storage_engines.local_fs.open', create=True)
    def test_put(self, mock_open, mock_shutil, mock_ensure_directory_path_exists):
        mock_source_file = MagicMock()

        test_destination_path = u'/some/directory/document.pdf'
        file_reference = LocalFSStorageEngine().put(
            test_destination_path, mock_source_file, mime_type=u'application/pdf', bucket_name=u'test.cdn.host',
            agent=self.agent)

        self.assertIn('some/directory', mock_ensure_directory_path_exists.mock_calls[0][1][0])

        self.assertEqual(mock_shutil.copyfileobj.mock_calls[0][1][0], mock_source_file)

    @patch('shared.file_storage.storage_engines.local_fs.BytesIO')
    @patch('shared.file_storage.storage_engines.local_fs.open', create=True)
    def test_get(self, mock_open, MockBytesIO):
        mock_file = MagicMock(name=u'mock_file')

        mock_file_content = MagicMock(name=u'mock_file_content')
        mock_file.read.return_value = mock_file_content

        mock_open.return_value.__enter__.return_value = mock_file

        mock_bytes_buffer = MagicMock(name=u'mock_bytes_buffer')
        MockBytesIO.return_value = mock_bytes_buffer

        actual_bytes_buffer = LocalFSStorageEngine().get(u'/some/directory/document.pdf')

        MockBytesIO.assert_called_with(mock_file_content)
        self.assertEqual(actual_bytes_buffer, mock_bytes_buffer)
