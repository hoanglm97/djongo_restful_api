from django.conf.urls import url
from students import views


urlpatterns = [
    url(r'^v1/api/register$', views.register),
    url(r'^v1/api/login$', views.login_required),
    url(r'^v1/api/students$', views.list_students),
    url(r'^v1/api/students/(?P<pk>[0-9]+)$', views.profile),
    url(r'^v1/api/students/all$', views.all_list_students)
]