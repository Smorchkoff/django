# Generated by Django 4.2.6 on 2024-01-10 14:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('birth_date', models.DateField()),
                ('death_date', models.DateField()),
                ('description', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Print',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=100)),
                ('foundation_date', models.DateField()),
                ('description', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('author', models.CharField(max_length=50)),
                ('desctiption', models.CharField(max_length=500)),
                ('print', models.CharField(max_length=100)),
                ('pub_date', models.DateField()),
                ('language', models.CharField(max_length=50)),
                ('ISBN', models.CharField(max_length=17)),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ChitayGorod.genre')),
            ],
        ),
    ]
