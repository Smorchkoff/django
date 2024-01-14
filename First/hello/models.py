from django.db import models
from django import forms


# Create your models here.

class Person(models.Model):
    name = models.CharField(max_length=20)
    age = models.IntegerField()


class UserManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter()


class UserModel(models.Model):
    login = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.login

    class Meta:
        verbose_name = "Зарегистрированные пользователи"
        verbose_name_plural = "Зарегистрированные пользователи"
        ordering = ['login']
        indexes = [
            models.Index(fields=['login'])
        ]
