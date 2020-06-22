from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from node import views

urlpatterns = [
    url(r'^status$', views.status),
    url(r'^version', views.version),
    url(r'(?P<project>.*)/(?P<test_id>.*)/start', views.job_start),
    url(r'^test/rawlog/(?P<logid>\d+)/$', views.test_run_raw_log),
    url(r'^test/log/(?P<logid>\d+)/$', views.test_run_log),
    url(r'^test/log/(?P<logid>\d+)/delete$', views.test_run_log_delete),
]
