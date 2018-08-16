from django.conf.urls import url

from .views import (
    CommentListAPIView,
    CommentDetailAPIView
)


urlpatterns = [
    url(r'^$', CommentListAPIView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$', CommentDetailAPIView.as_view(), name='detail'),
    # url(r'^(?P<pk>\d+)/delete/$', comment_delete, name='delete'),
]
