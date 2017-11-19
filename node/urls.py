from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from node import views

urlpatterns = [
                  url(r'(?P<project>.*)/(?P<test_id>.*)/start', views.job_start),
              ]