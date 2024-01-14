from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.ManyToManyField('Author', related_name='author')
    description = models.CharField(max_length=500)
    print = models.CharField(max_length=100)
    pub_date = models.DateField()
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    language = models.ManyToManyField('Language', related_name='lang')
    ISBN = models.CharField(max_length=17)

    def __str__(self):
        return self.title


class Author(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField()
    death_date = models.DateField()
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=50, db_index=True)

    def __str__(self):
        return self.name


class Print(models.Model):
    name = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    foundation_date = models.DateField()
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=50, db_index=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.FileField(upload_to='profile_pics/', null=True, verbose_name='')
    city = models.CharField(max_length=100)
    birth = models.DateField(null=True)
    bio = models.TextField(max_length=500, null=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
# class CustomUser(AbstractUser):
#     photo = models.ImageField()
#     city = models.CharField(max_length=100)
#     birth = models.DateField()
#     bio = models.TextField(max_length=500)
