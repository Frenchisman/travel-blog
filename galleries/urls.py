from django.conf.urls import url

from . import views

app_name = 'galleries'
urlpatterns = [
    # Ex : /galleries/
    url(r'^$', views.gallery_list, name='gallery_list'),
    # Ex : /galleries/5
    url(r'^(?P<gallery_id>[0-9]+)/$', views.gallery_detail,
        name='gallery_detail')
]
