from django.conf.urls import url

from .views import (
    CommentCreateAPIView,
    CommentDetailAPIView,
    CommentEditAPIView,
    CommentListAPIView,
)


urlpatterns = [
    url(r'^$', CommentListAPIView.as_view(), name='list'),
    url(r'^create/$', CommentCreateAPIView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$', CommentDetailAPIView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/edit/$', CommentEditAPIView.as_view(), name='edit'),
]
