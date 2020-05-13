from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader

from forum import pwd_helper
from forum.models import User, UserSettings


def get_user(request):
    try:
        user_id = request.session['user_id']
        user = User.objects.filter(id=user_id).first()
    except KeyError:
        user = None
    return user


def get_language(request):
    try:
        language = request.session['language']
    except KeyError:
        language = None
    return language


def set_lang_pl(request):
    request.session['language'] = 'pl'
    try:
        user_id = request.session['user_id']
        user = User.objects.filter(id=user_id).first()
    except KeyError:
        user = None
    if user is not None:
        user_settings = UserSettings(user=user, language='pl')
        user_settings.save()
    return redirect('/')


def set_lang_en(request):
    request.session['language'] = 'en'
    try:
        user_id = request.session['user_id']
        user = User.objects.filter(id=user_id).first()
    except KeyError:
        user = None
    if user is not None:
        user.language = 'en'
        user.save()
    return redirect('/')


def register(request):
    language = get_language(request)
    template = loader.get_template('auth/register.html')
    error = None

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if not username:
            if language == 'pl':
                error = 'Musisz podać nazwę użytkownik.'
            else:
                error = 'Username is required.'
        elif not password:
            if language == 'pl':
                error = 'Musisz podać hasło.'
            else:
                error = 'Password is required.'
        elif User.objects.filter(username=username).count() > 0:
            if language == 'pl':
                error = 'Użytkownik {} jest już zarejestrowany.'.format(username)
            else:
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
        'user': None,
        'language': language
    }

    return HttpResponse(template.render(context, request))


def login(request):
    language = get_language(request)
    template = loader.get_template('auth/login.html')
    error = None

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.filter(username=username).first()

        if user is None:
            if language == 'pl':
                error = 'Nieprawidłowa nazwa użytkownika.'
            else:
                error = 'Incorrect username.'
        elif not pwd_helper.verify_password(stored_password=user.password, provided_password=password):
            if language == 'pl':
                error = 'Nieprawidłowe hasło.'
            else:
                error = 'Incorrect password.'
        if error is None:
            request.session.clear()
            request.session['user_id'] = user.id
            user_settings = UserSettings.objects.filter(user=user).first()
            if user_settings is not None:
                request.session['language'] = user_settings.language
            return redirect('/')

    errors = []
    if error is not None:
        errors.append(error)
    context = {
        'error_messages': errors,
        'user': None,
        'language': language
    }

    return HttpResponse(template.render(context, request))


def logout(request):
    request.session.clear()
    return redirect('/')
