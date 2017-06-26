# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.db.models import Count
from ..log_reg.models import Users

class SecretManager(models.Manager):
    def add_secret(self, postData, user_id):
        if len(postData["secret"]) < 1:
            return (False, "Cannot post an empty secret!")
        else:
            user = Users.objects.get(id=user_id)
            secret = self.create(post = postData["secret"], user = user)
            return (True, "Your secret is safe with us.")

    def recent(self, num_secrets):
        return Secrets.objects.order_by("-created_at")[:num_secrets].annotate(num_likes=Count("secret_for_like"))

    def popular(self):
        return Secrets.objects.annotate(num_likes=Count("secret_for_like")).order_by("-num_likes")

class LikeManager(models.Manager):
    def add_like(self, user_id, secret_id):
        user = Users.objects.get(id=user_id)
        secret = Secrets.objects.get(id=secret_id)
        if self.filter(user=user, secret=secret):
            return
        elif self.filter(user=user):
            self.get(user=user).secret.add(secret)
        else:
            newSecret = self.create(user=user)
            newSecret.secret.add(secret)


# Create your models here.
class Secrets(models.Model):
    post = models.TextField()
    user = models.ForeignKey(Users, related_name="user_for_secret")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = SecretManager()

class Likes(models.Model):
    secret = models.ManyToManyField(Secrets, related_name="secret_for_like")
    user = models.OneToOneField(Users, related_name="user_for_like")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = LikeManager()