from unittest import loader

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from ChitayGorod import forms
from ChitayGorod.models import Book, Author, Language, Profile
from ChitayGorod.forms import RegisterForm, LoginForm, AddBookForm, edit_form, UserForm, ChangePasswordForm, \
    ChangeEmailForm, ChangeLoginForm


# Create your views here.

def index(request):
    return render(request, 'catalog.html')


def showBooks(request):
    sort_by = request.GET.get('sort_by') or "title"

    books_sorted = Book.objects.all().order_by(sort_by)
    print(f'Sort_by == {sort_by}')
    print(books_sorted)
    return render(request, 'books.html', {"books": books_sorted, "sort_by": sort_by})


def showAuthors(request):
    authors = Author.objects.all()
    return render(request, 'authors.html', {"authors": authors})


def showAuthor(request, author_id):
    try:
        author = Author.objects.get(pk=author_id)
    except Author.DoesNotExist:
        return render(request, 'warning.html')

    return render(request, 'author.html', context={'author': author})


def showBook(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return render(request, 'warning.html')
    return render(request, 'book.html', context={'book': book})


def login_user(request):
    if request.method == 'POST':

        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user and user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('catalog'))
    else:
        form = LoginForm()
    return render(request, 'login.html', context={'form': form})


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return HttpResponseRedirect(reverse('login'))
    else:
        form = RegisterForm()
    return render(request, 'register.html', context={'form': form})


def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, user=request.user)
        if form.is_valid():
            cd = form.cleaned_data

            if check_password(cd['old_password'], request.user.password):
                user = User.objects.get(id=request.user.id)
                user.set_password(cd['new_password'])
                user.save(update_fields=['password'])
            else:
                messages.error(request, 'Invalid pass')
                return render(request, 'change_password.html', context={'form': form, 'flag': True})
            return HttpResponseRedirect(reverse('login'))
    else:
        form = ChangePasswordForm(instance=request.user)
    return render(request, 'change_password.html', context={"form": form, 'flag': False})


def change_email(request):
    if request.method == 'POST':
        form = ChangeEmailForm(request.POST, user=request.user)
        if form.is_valid():
            cd = form.cleaned_data
            if check_password(cd['password'], request.user.password):
                user = User.objects.get(id=request.user.id)
                if cd['email'] != request.user.email:
                    user.email = cd['email']
                    user.save(update_fields=['email'])
            else:
                messages.error(request, 'Invalid pass')
                return render(request, 'change_email.html', context={'form': form, 'flag': True})
            return HttpResponseRedirect(reverse('profile'))
    else:
        form = ChangeEmailForm(instance=request.user)
    return render(request, 'change_email.html', context={"form": form, 'flag': False})


def change_login(request):
    if request.method == 'POST':
        form = ChangeLoginForm(request.POST, user=request.user)
        if form.is_valid():
            cd = form.cleaned_data
            if check_password(cd['password'], request.user.password):
                user = User.objects.get(id=request.user.id)
                if cd['username'] != request.user.username:
                    user.username = cd['username']
                    user.save(update_fields=['username'])
            else:
                messages.error(request, 'Invalid pass')
                return render(request, 'change_email.html', context={'form': form, 'flag': True})
            return HttpResponseRedirect(reverse('profile'))
    else:
        form = ChangeLoginForm(instance=request.user)
    return render(request, 'change_login.html', context={"form": form, 'flag': False})


def edit_profile(request):
    if request.method == 'POST':
        user = UserForm(request.POST, instance=request.user)
        profile = edit_form(request.POST, request.FILES, instance=request.user.profile)
        if user.is_valid() and profile.is_valid():
            # cd = form.cleaned_data
            # user = request.user
            # user.first_name = cd['first_name']
            # user.last_name = cd['last_name']
            # # userprofile = Profile(user=user)
            # user.profile.bio = cd['bio']
            # user.profile.birth = cd['birth']
            # user.profile.city = cd['city']

            user.save()

            profile.photo = ''
            profile.save()
            return HttpResponseRedirect(reverse('profile'))
    userform = UserForm(instance=request.user)
    profileForm = edit_form(instance=request.user.profile)
    return render(request, 'profile_edit.html', context={''
                                                         'UserForm': userform,
                                                         'ProfileForm': profileForm
                                                         })


def book_create(request):
    if request.user.is_staff:
        form = AddBookForm()
        return render(request, 'book_create.html', context={'form': form})
    else:
        return HttpResponseRedirect(reverse('catalog'))


def show_favorite_books(request):
    return render(request, 'favourites.html')


def show_profile(request):
    profile = Profile.objects.filter(user=request.user)
    return render(request, 'profile.html', context={'profile': profile})
