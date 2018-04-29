from django.conf.urls import url

from .views import (
    PostListAPIView,
    PostDeleteAPIView,
    PostUpdateAPIView,
    PostDetailAPIView,
    PostCreateAPIView
)


urlpatterns = [
    url(r'^$', PostListAPIView.as_view(), name='list'),
    url(r'^create/$', PostCreateAPIView.as_view(), name='create'),
    url(r'^(?P<slug>[\w\-]+)/$', PostDetailAPIView.as_view(), name='detail'),
    url(r'^(?P<slug>[\w\-]+)/edit/$', PostUpdateAPIView.as_view(), name='update'),
    url(r'^(?P<slug>[\w\-]+)/delete/$', PostDeleteAPIView.as_view(), name='delete'),
]
