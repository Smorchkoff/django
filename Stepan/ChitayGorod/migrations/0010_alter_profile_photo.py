# Generated by Django 4.2.6 on 2024-01-13 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ChitayGorod', '0009_alter_profile_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.FileField(null=True, upload_to='static/images/profile_pics', verbose_name=''),
        ),
    ]