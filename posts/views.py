from django.http import HttpResponse
from django.shortcuts import render


def post_create(request):
    return HttpResponse('<h1>Create</h1>')


def post_retrieve(request):
    return HttpResponse('<h1>Retrieve</h1>')


def post_list(request):
    return HttpResponse('<h1>List</h1>')


def post_update(request):
    return HttpResponse('<h1>Update</h1>')


def post_delete(request):
    return HttpResponse('<h1>Hello</h1>')
