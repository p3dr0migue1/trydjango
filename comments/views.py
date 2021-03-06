from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404

from .forms import CommentForm
from .models import Comment


@login_required
def comment_delete(request, id):
    try:
        comment = Comment.objects.get(id=id)
    except:
        raise Http404

    if comment.user != request.user:
        messages.warning(request, "You do NOT have permission to view this comment.")
        raise Http404
    
    if request.method == 'POST':
        parent_obj_url = comment.content_object.get_absolute_url()
        comment.delete()
        messages.success(request, "Comment has been successfully deleted.")
        return HttpResponseRedirect(parent_obj_url)

    context = {
       'object': comment 
    }
    return render(request, 'comment_delete.html', context)

def comment_thread(request, id):
    try:
        comment = Comment.objects.get(id=id)
    except:
        raise Http404

    if not comment.is_parent:
        comment = comment.parent

    content_object = comment.content_object  # Post that the comment is on
    content_id = comment.content_object.id

    initial_data = {
        'content_type': comment.content_type,
        'object_id': comment.object_id
    }
    
    comment_form = CommentForm(request.POST or None, initial=initial_data)
    
    if comment_form.is_valid() and request.user.is_authenticated():
        c_type = comment_form.cleaned_data.get('content_type')
        content_type = ContentType.objects.get(model=c_type)
        obj_id = comment_form.cleaned_data.get('object_id')
        content_data = comment_form.cleaned_data.get('content')
        parent_obj = None

        try:
            parent_id = int(request.POST.get('parent_id'))
        except:
            parent_id = None

        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists:
                parent_obj = parent_qs.first()

        new_comment, created = Comment.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=obj_id,
            content=content_data,
            parent=parent_obj,
        )
        # instead of redirecting to the post page, we want to redirect
        # the user to the thread page
        return HttpResponseRedirect(parent_obj.get_absolute_url())
    
    context = {
        'comment': comment,
        'comment_form': comment_form, 
    }
    return render(request, 'comment_thread.html', context)
