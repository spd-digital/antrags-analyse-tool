from rest_framework import serializers
from shared.email.models import EmailMessage, EmailAddress, EmailAttachment
from shared.file_storage.models import FileReference


class FileReferenceSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    file_name = serializers.CharField()
    path = serializers.CharField()
    mime_type = serializers.CharField()
    storage_engine = serializers.CharField()

    class Meta:
        model = FileReference
        fields = ['id', ]


class EmailAddressSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    name = serializers.CharField()
    address = serializers.CharField()

    class Meta:
        model = EmailAddress
        fiels = ['id', 'name', 'address']


class EmailAttachmentSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    file_reference = FileReferenceSerializer()

    class Meta:
        model = EmailAttachment
        fields = ['id', 'email_message', 'file_reference']


class EmailMessageFullDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    sender = EmailAddressSerializer()
    recipients = EmailAddressSerializer(many=True)

    text = serializers.CharField()
    html = serializers.CharField()

    emailattachment_set = EmailAttachmentSerializer(many=True)

    raw_email_content = FileReferenceSerializer()

    class Meta:
        model = EmailMessage
        fiels = ['id', 'sender', 'recipients', 'text', 'html', 'emailattachment_set', 'raw_email_content']
