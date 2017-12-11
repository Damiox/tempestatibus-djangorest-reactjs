from django.conf.urls import url, include
from django.views import generic
from django.contrib import admin
from rest_framework import routers
from tempestatibus.api import views

#router = routers.DefaultRouter()
#router.register(r'subscription/confirm', views.ConfirmSubscriptionViewSet, base_name="ConfirmSubscription")
#router.register(r'subscription', views.ConfirmSubscriptionViewSet, base_name="ConfirmSubscription")

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    #url(r'^api-router/', include(router.urls)),
    #url(r'^api/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/v1/location', views.LocationView.as_view()),
    url(r'^api/v1/subscription$', views.SubscribeReceiptView.as_view()),
    url(r'^api/v1/subscription/(?P<confirmation_id>[0-9a-z]{32})/confirm', views.ConfirmSubscriptionView.as_view()),
    url(r'^admin/', admin.site.urls),
    url(r'^', generic.TemplateView.as_view(template_name="index.html"))
]
