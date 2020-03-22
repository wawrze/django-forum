from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader

from forum import pwd_helper
from forum.models import User


def get_user(request):
    try:
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
    except KeyError:
        user = None
    return user


def register(request):
    template = loader.get_template('auth/register.html')
    error = None

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif User.objects.filter(username=username).count() > 0:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            user = User(username=username, password=pwd_helper.hash_password(password))
            user.save()
            return redirect('/login/')

    errors = []
    if error is not None:
        errors.append(error)
    context = {
        'error_messages': errors,
        'user': None
    }

    return HttpResponse(template.render(context, request))


def login(request):
    template = loader.get_template('auth/login.html')
    error = None

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.get(username=username)

        if user is None:
            error = 'Incorrect username.'
        elif not pwd_helper.verify_password(stored_password=user.password, provided_password=password):
            error = 'Incorrect password.'
        if error is None:
            request.session.clear()
            request.session['user_id'] = user.id
            return redirect('/')

    errors = []
    if error is not None:
        errors.append(error)
    context = {
        'error_messages': errors,
        'user': None
    }

    return HttpResponse(template.render(context, request))


def logout(request):
    request.session.clear()
    return redirect('/')
