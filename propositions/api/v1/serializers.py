from propositions.models import ProtoProposition
from rest_framework import serializers
from shared.api.v1.serializers import EmailMessageFullDetailSerializer


class ProtoPropositionSerializer(serializers.Serializer):
    class Meta:
        model = ProtoProposition


class ProtoPropositionFullDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    email_message = EmailMessageFullDetailSerializer()

    class Meta:
        model = ProtoProposition
        fields = ['id', 'email_message']
