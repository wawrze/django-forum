from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader

from forum.models import *
from forum.views.auth import get_user


def general(request):
    logged_user = get_user(request)

    try:
        oldest_post_date = Post.objects.latest('created').created
    except Post.DoesNotExist:
        oldest_post_date = now()
    days = (now() - oldest_post_date).days
    if days == 0:
        days = 1
    posts_count = Post.objects.count()
    if posts_count == 0:
        posts_count = 1
    comments_count = Comment.objects.count()

    try:
        post_titles = Post.objects.values('title').all()
        posts_bodies = Post.objects.values('body').all()
        comment_bodies = Comment.objects.values('body').all()
        all_texts = ''
        for i in range(posts_count):
            all_texts += ' '
            all_texts += post_titles[i]['title']
            all_texts += ' '
            all_texts += posts_bodies[i]['body']
        for i in range(comments_count):
            all_texts += ' '
            all_texts += comment_bodies[i]['body']
        chars_count = len(all_texts)
        words_count = len(all_texts.split())
    except Post.DoesNotExist:
        words_count = 1
        chars_count = 1

    users_count = User.objects.count()
    if users_count == 0:
        users_count = 1

    posts_per_day = round(posts_count / days, 2)
    posts_per_user = round(posts_count / users_count, 2)
    words_per_post_and_comment = round(words_count / (posts_count + comments_count), 2)
    words_per_day = round(words_count / days, 2)
    words_per_user = round(words_count / users_count, 2)
    chars_per_post_and_comment = round(chars_count / (posts_count + comments_count), 2)
    chars_per_day = round(chars_count / days, 2)
    chars_per_user = round(chars_count / users_count, 2)
    comments_per_post = round(comments_count / posts_count, 2)
    comments_per_day = round(comments_count / days, 2)
    comments_per_user = round(comments_count / users_count, 2)

    template = loader.get_template('stats/general_stats.html')
    context = {
        'user': logged_user,
        'errors': [],
        'days': days,
        'posts_count': posts_count,
        'users_count': users_count,
        'comments_count': comments_count,
        'words_count': words_count,
        'chars_count': chars_count,
        'posts_per_day': posts_per_day,
        'posts_per_user': posts_per_user,
        'comments_per_post': comments_per_post,
        'comments_per_day': comments_per_day,
        'comments_per_user': comments_per_user,
        'words_per_post_and_comment': words_per_post_and_comment,
        'words_per_day': words_per_day,
        'words_per_user': words_per_user,
        'chars_per_post_and_comment': chars_per_post_and_comment,
        'chars_per_day': chars_per_day,
        'chars_per_user': chars_per_user,
    }
    return HttpResponse(template.render(context, request))


def user(request, user_id):
    logged_user = get_user(request)

    stats_owner = User.objects.get(id=user_id)
    if stats_owner is None:
        return redirect('/login')

    days = (now() - stats_owner.created).days
    if days == 0:
        days = 1

    user_posts_count = Post.objects.filter(author=stats_owner).count()
    if user_posts_count == 0:
        user_posts_count = 1

    user_comments_count = Comment.objects.filter(author=stats_owner).count()

    try:
        post_titles = Post.objects.filter(author=stats_owner).values('title').all()
        posts_bodies = Post.objects.filter(author=stats_owner).values('body').all()
        comments_bodies = Comment.objects.filter(author=stats_owner).values('body').all()
        all_texts = ''
        for i in range(user_posts_count):
            all_texts += ' '
            all_texts += post_titles[i]['title']
            all_texts += ' '
            all_texts += posts_bodies[i]['body']
        for i in range(user_comments_count):
            all_texts += ' '
            all_texts += comments_bodies[i]['body']
        user_chars_count = len(all_texts)
        user_words_count = len(all_texts.split())
    except Post.DoesNotExist:
        user_words_count = 1
        user_chars_count = 1

    posts_per_day = round(user_posts_count / days, 2)
    words_per_post_and_comment = round(user_words_count / (user_posts_count + user_comments_count), 2)
    words_per_day = round(user_words_count / days, 2)
    chars_per_post_and_comment = round(user_chars_count / (user_posts_count + user_comments_count), 2)
    chars_per_day = round(user_chars_count / days, 2)
    comments_per_day = round(user_comments_count / days, 2)

    template = loader.get_template('stats/user_stats.html')
    context = {
        'user': logged_user,
        'errors': [],
        'days': days,
        'stats_owner': stats_owner,
        'posts_count': user_posts_count,
        'words_count': user_words_count,
        'comments_count': user_comments_count,
        'chars_count': user_chars_count,
        'posts_per_day': posts_per_day,
        'comments_per_day': comments_per_day,
        'words_per_post_and_comment': words_per_post_and_comment,
        'words_per_day': words_per_day,
        'chars_per_post_and_comment': chars_per_post_and_comment,
        'chars_per_day': chars_per_day
    }
    return HttpResponse(template.render(context, request))
