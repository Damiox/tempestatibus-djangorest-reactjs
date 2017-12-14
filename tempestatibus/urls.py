from django.views import generic
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.views.decorators.csrf import ensure_csrf_cookie
from tempestatibus.api import views

# Removing first slash as it is unnecessary
urlPrefix = r'^' + settings.API_BASE_PREFIX[1:]

# Url definitions for the Rest API and the web content
urlpatterns = [
    url(urlPrefix
        + r'/location$',
        ensure_csrf_cookie(views.LocationView.as_view()),
        name='location'),
    url(urlPrefix
        + r'/subscription$',
        ensure_csrf_cookie(views.SubscribeReceiptView.as_view()),
        name='subscription'),
    url(urlPrefix
        + r'/unsubscription$',
        ensure_csrf_cookie(views.UnsubscribeReceiptView.as_view()),
        name='unsubscription'),
    url(urlPrefix
        + r'/subscription/(?P<confirmation_id>[0-9a-z-]{36})/confirm$',
        ensure_csrf_cookie(views.ConfirmSubscriptionView.as_view()),
        name='confirm-subscription'),
    url(urlPrefix
        + r'/unsubscription/(?P<confirmation_id>[0-9a-z-]{36})/confirm$',
        ensure_csrf_cookie(views.ConfirmUnsubscriptionView.as_view()),
        name='confirm-unsubscription'),
    url(r'^/admin/',
        admin.site.urls),
    url(r'^',
        ensure_csrf_cookie(generic.TemplateView.as_view(
            template_name="index.html")))
]
