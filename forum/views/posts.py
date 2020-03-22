from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.utils import timezone

from forum.models import Post
from forum.views.auth import get_user


def index(request):
    posts = Post.objects.order_by('-created')
    template = loader.get_template('posts/index.html')
    context = {
        'posts': posts,
        'user': get_user(request)
    }
    return HttpResponse(template.render(context, request))


def create(request):
    user = get_user(request)
    if user is None:
        redirect('/login')

    error = None
    title = None
    body = None
    if request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']
        if not title:
            error = 'Title is required.'
        else:
            post = Post(title=title, body=body, author=user)
            post.save()
            return redirect('/')

    errors = []
    if error is not None:
        errors.append(error)
    template = loader.get_template('posts/create.html')
    context = {
        'user': user,
        'errors': errors,
        'title': title,
        'body': body
    }
    return HttpResponse(template.render(context, request))


def update(request, post_id):
    user = get_user(request)
    if user is None:
        return redirect('/login')

    try:
        post = Post.objects.get(id=post_id)
        if post.id != post_id:
            return redirect('/')
    except Post.DoesNotExist:
        return redirect('/')

    error = None
    if request.method == 'POST':
        post.title = request.POST['title']
        post.body = request.POST['body']
        if not post.title:
            error = 'Title is required.'
        else:
            post.modification = timezone.now()
            post.save()
            return redirect('/')

    errors = []
    if error is not None:
        errors.append(error)
    template = loader.get_template('posts/update.html')
    context = {
        'user': user,
        'errors': errors,
        'post': post
    }
    return HttpResponse(template.render(context, request))


def delete(request, post_id):
    user = get_user(request)
    if user is None:
        redirect('login')

    try:
        post = Post.objects.get(id=post_id)
        if post.id != post_id:
            return redirect('/')
        post.delete()
        return redirect('/')
    except Post.DoesNotExist:
        return redirect('/')
