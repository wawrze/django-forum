from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now


class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    language = models.CharField(max_length=2, null=True)


class Post(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    created = models.DateTimeField(null=False, default=now)
    modification = models.DateTimeField(null=True)
    title = models.CharField(max_length=30, null=False)
    body = models.CharField(max_length=200, null=False)

    @property
    def create_date(self):
        return self.created.strftime('%Y-%m-%d %H:%M')

    @property
    def modified(self):
        return self.modification.strftime('%Y-%m-%d %H:%M')

    @property
    def comment_count(self):
        return self.comment_set.count()


class Comment(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False)
    created = models.DateTimeField(null=False, default=now)
    modification = models.DateTimeField(null=True)
    body = models.CharField(max_length=50, null=False)

    @property
    def create_date(self):
        return self.created.strftime('%Y-%m-%d %H:%M')

    @property
    def modified(self):
        return self.modification.strftime('%Y-%m-%d %H:%M')
