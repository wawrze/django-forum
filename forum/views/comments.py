from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.utils import timezone

from forum.models import Post, Comment
from forum.views.auth import get_user, get_language


def add(request, post_id):
    language = get_language(request)
    user = get_user(request)
    if user is None:
        redirect('/login')
    try:
        post = Post.objects.get(id=post_id)
        if post.id != post_id:
            return redirect('/')
    except Post.DoesNotExist:
        return redirect('')

    error = None
    body = None
    if request.method == 'POST':
        body = request.POST['body']
        if not body:
            if language == 'pl':
                error = 'Musisz podac treść komentarza.'
            else:
                error = 'Comment body is required.'
        else:
            comment = Comment(post=post, body=body, author=user)
            comment.save()
            return redirect('/')

    errors = []
    if error is not None:
        errors.append(error)
    template = loader.get_template('posts/comments/add.html')
    context = {
        'post': post,
        'user': user,
        'errors': errors,
        'body': body,
        'language': language
    }
    return HttpResponse(template.render(context, request))


def edit(request, post_id, comment_id):
    language = get_language(request)
    user = get_user(request)
    if user is None:
        return redirect('/login')

    try:
        post = Post.objects.get(id=post_id)
        if post.id != post_id:
            return redirect('/')
    except Post.DoesNotExist:
        return redirect('/')

    try:
        comment = Comment.objects.get(id=comment_id)
        if comment.id != comment_id:
            return redirect('/')
    except Comment.DoesNotExist:
        return redirect('/')

    error = None
    if request.method == 'POST':
        comment.body = request.POST['body']
        if not comment.body:
            if language == 'pl':
                error = 'Musisz podac treść komentarza.'
            else:
                error = 'Comment body is required.'
        else:
            comment.modification = timezone.now()
            comment.save()
            return redirect('/')

    errors = []
    if error is not None:
        errors.append(error)
    template = loader.get_template('posts/comments/edit.html')
    context = {
        'comment': comment,
        'user': user,
        'errors': errors,
        'post': post,
        'language': language
    }
    return HttpResponse(template.render(context, request))


def delete(request, post_id, comment_id):
    user = get_user(request)
    if user is None:
        redirect('login')

    try:
        comment = Comment.objects.get(id=comment_id)
        if comment.id != comment_id:
            return redirect('/')
        comment.delete()
        return redirect('/')
    except Comment.DoesNotExist:
        return redirect('/')
