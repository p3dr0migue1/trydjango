from django.conf.urls import url

from .views import (
    post_create, post_retrieve, post_list,
    post_update, post_delete
)


urlpatterns = [
    url(r'^create/$', post_create),
    url(r'^retrieve/$', post_retrieve),
    url(r'^list/$', post_list),
    url(r'^update/$', post_update),
    url(r'^delete/$', post_delete),
]
