from django.contrib import admin
from django.urls import path

from forum.views import stat, auth, posts, comments

urlpatterns = [
    path('', posts.index, name='index'),
    path('admin/', admin.site.urls),
    path('register/', auth.register, name='register'),
    path('login/', auth.login, name='login'),
    path('logout/', auth.logout, name='logout'),
    path('stat/general/', stat.general, name='general'),
    path('stat/user/<int:user_id>/', stat.user, name='user'),
    path('post/create/', posts.create, name='create'),
    path('post/<int:post_id>/update/', posts.update, name='update'),
    path('post/<int:post_id>/delete/', posts.delete, name='delete'),
    path('post/<int:post_id>/comments/add', comments.add, name='add'),
    path('post/<int:post_id>/comments/<int:comment_id>/edit', comments.edit, name='add'),
    path('post/<int:post_id>/comments/<int:comment_id>/delete', comments.delete, name='add'),
    path('set/pl', auth.set_lang_pl, name='set_pl'),
    path('set/en', auth.set_lang_en, name='set_en')
]
