"""Propositions API views."""

import json

from django.contrib.auth.models import AnonymousUser
from propositions.api.v1.serializers import ProtoPropositionSerializer, ProtoPropositionFullDetailSerializer
from propositions.models import ProtoProposition
from propositions.processes.submit_by_email import submit_proposition_by_emails
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from shared.mandrill.tools import get_sender_emails, save_raw_email_message, persist_email_messages


class PropositionMailbox(APIView):
    def get(self, request, *args, **kwargs):
        return Response()

    def post(self, request, *args, **kwargs):
        """Endpoint for Mandrill's inbound mail service.

        Args:
            request:
            *args:
            **kwargs:

        Returns:

        """

        # try to extract the sender email before any other processing so that we can give mail-based error feedback
        sender_emails = get_sender_emails(request.data)

        # save raw email message
        agent = request.user if not isinstance(request.user, AnonymousUser) else None
        email_content = save_raw_email_message(json.dumps(request.data), agent=agent)

        # persist email messages
        try:
            email_messages = persist_email_messages(request.data)
            submit_proposition_by_emails(email_messages)
        except Exception as e:
            raise

        return Response()


class ProtoPropositionListView(ListAPIView):
    """Endpoint returning a list of proto propositions."""
    queryset = ProtoProposition.objects.all()
    serializer_class = ProtoPropositionFullDetailSerializer


class ProtoPropositionDetailView(APIView):
    def get(self, request, pk=None):
        """Endpoint returning information about an individual proto proposition.

        Args:
            request:
            pk:

        Returns:

        """
        if not pk:
            raise ParseError(detail=u'no primary key provided')
        try:
            proto_proposition = ProtoProposition.objects.get(pk=pk)
        except ProtoProposition.DoesNotExist:
            raise NotFound(detail=u'no proto proposition found for primary key {}'.format(pk))
        return Response(ProtoPropositionFullDetailSerializer(proto_proposition).data)
