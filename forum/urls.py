from django.urls import path

from forum.views import stat, auth, posts

urlpatterns = [
    path('', posts.index, name='index'),
    path('register/', auth.register, name='register'),
    path('login/', auth.login, name='login'),
    path('logout/', auth.logout, name='logout'),
    path('stat/general/', stat.general, name='general'),
    path('stat/user/<int:user_id>/', stat.user, name='user'),
    path('post/create/', posts.create, name='create'),
    path('post/<int:post_id>/update/', posts.update, name='update'),
    path('post/<int:post_id>/delete/', posts.delete, name='delete'),
]
