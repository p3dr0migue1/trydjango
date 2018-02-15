from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^create/$', "posts.views.post_create"),
    url(r'^retrieve/$', "posts.views.post_retrieve"),
    url(r'^list/$', "posts.views.post_list"),
    url(r'^update/$', "posts.views.post_update"),
    url(r'^delete/$', "posts.views.post_delete"),
]
