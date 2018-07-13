from django.conf.urls import url

from .views import request_test_view

urlpatterns = [
    url(r'^$', request_test_view, name='request-test'),
]
