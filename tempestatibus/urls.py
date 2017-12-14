from django.views import generic
from django.conf.urls import url
from django.contrib import admin
from tempestatibus.api import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^api/v1/location',
        views.LocationView.as_view(), name='location'),
    url(r'^api/v1/subscription$',
        views.SubscribeReceiptView.as_view(), name='subscription'),
    url(r'^api/v1/subscription/(?P<confirmation_id>[0-9a-z-]{36})/confirm',
        views.ConfirmSubscriptionView.as_view(), name='confirm-subscription'),
    url(r'^admin/',
        admin.site.urls),
    url(r'^',
        generic.TemplateView.as_view(template_name="index.html"))
]
