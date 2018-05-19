from django.conf.urls import url
from propositions.api.v1.views import PropositionMailbox, ProtoPropositionDetailView, ProtoPropositionListView

urlpatterns = [
    url(r'mailbox/', PropositionMailbox.as_view(), name='mailbox'),
    url(r'proto/(?P<pk>[0-9]+)/', ProtoPropositionDetailView.as_view(), name='proto_proposition'),
    url(r'proto/', ProtoPropositionListView.as_view(), name='proto_propositions'),
]
