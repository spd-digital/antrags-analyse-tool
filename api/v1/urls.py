from django.conf.urls import url, include


urlpatterns = [
    url(r'propositions/', include('propositions.api.v1.urls', namespace='propositions')),
]