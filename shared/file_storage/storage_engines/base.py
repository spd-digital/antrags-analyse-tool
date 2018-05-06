import arrow
from shared.file_storage.models import FileReference
from shared.models import DataUpdate
from shared.constants import DATA_UPDATE_STATUS_CREATED, MIME_TYPE_TEXT_PLAIN
from shared.tools import get_or_create_system_user


class StorageEngine(object):
    storage_engine = None

    def put(self, *args, **kwargs):
        """Persists a file to the storage engine.

        Args:
            *args:
            **kwargs:

        Returns (FileReference): database reference to the persisted file.

        """
        agent = kwargs.get('agent', get_or_create_system_user())
        timestamp = kwargs.get('timestamp', arrow.utcnow().datetime)
        mime_type = kwargs.get('mime_type', MIME_TYPE_TEXT_PLAIN)

        file_name, file_path = self._put(*args, **kwargs)

        return self._create_file_reference(file_name, file_path, mime_type, agent=agent, timestamp=timestamp)

    def _put(self, *args, **kwargs):
        """For implementation in child classes."""
        raise NotImplementedError()

    def _create_file_reference(self, file_name, file_path, mime_type, agent=None, timestamp=None):
        """Creates a reference to the persisted file in the database and return it.

        Args:
            file_name (unicode): (original) file name.
            file_path (unicode): full path to the persisted file, usually with a generated file name.
            mime_type (unicode): mime type of the file, ex. application/pdf.
            agent (User): Django user triggering the file persistence process.
            timestamp: when the file was persisted.

        Returns:

        """

        # create the data update
        data_update = DataUpdate(
            agent=agent, timestamp=timestamp, previous_status=None, status=DATA_UPDATE_STATUS_CREATED)
        data_update.save()

        # create the file reference
        file_reference = FileReference(
            file_name=file_name, path=file_path, mime_type=mime_type, storage_engine=self.storage_engine)
        file_reference.save()

        file_reference.status_changes.add(data_update)

        return file_reference

    def _generate_file_name(self, file_extension=None):
        """Generates a new filename."""
        from shared.file_storage.tools import generate_file_name
        return generate_file_name(file_extension=file_extension)
