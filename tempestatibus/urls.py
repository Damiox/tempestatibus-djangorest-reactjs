from django.conf.urls import url, include
from django.views import generic
from rest_framework import routers
from tempestatibus.api import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', generic.TemplateView.as_view(template_name="index.html")),
    url(r'^api-router/', include(router.urls)),
    url(r'^api/', include('rest_framework.urls', namespace='rest_framework'))
]
