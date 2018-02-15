from django.http import HttpResponse
from django.shortcuts import render

from .models import Post


def post_create(request):
    return render(request, 'index.html', {})


def post_retrieve(request):
    context = {'title': 'Detail'}
    return render(request, 'index.html', context)


def post_list(request):
    queryset = Post.objects.all()
    context = {'title': 'List', 'object_list': queryset}
    # if request.user.is_authenticated():
    #     context = {'title': 'My user list'}
    # else:
    #     context = {'title': 'List'}
    return render(request, 'index.html', context)


def post_update(request):
    return HttpResponse('<h1>Update</h1>')


def post_delete(request):
    return HttpResponse('<h1>Hello</h1>')
