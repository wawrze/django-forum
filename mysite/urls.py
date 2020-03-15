from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('forum/', include('forum.urls')),
    path('admin/', admin.site.urls),
]
