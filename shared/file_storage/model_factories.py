import factory
from shared.file_storage.models import FileReference
from shared.model_factories import DataUpdateFactory


class FileReferenceFactory(factory.DjangoModelFactory):
    class Meta:
        model = FileReference

    file_name = u'Antragsdatei.pdf'
    path = u'antraege-uploads/antraege/163655/3975605767.pdf'
    mime_type = u'application/pdf'
    storage_engine = u'aws_s3'

    #status_changes = factory.SubFactory(DataUpdateFactory)
