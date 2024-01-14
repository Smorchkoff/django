import string

from django import forms

from django.contrib.auth import get_user_model
from ChitayGorod.models import Language, Genre, Profile
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
import re
from string import punctuation


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    username = forms.CharField(label='Логин', widget=forms.TextInput())
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput())
    email = forms.EmailField(label='Электронная почта', widget=forms.EmailInput())

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password', 'password2', ]

        # widgets = {
        #     'username': forms.TextInput(attrs={'class': 'reg'}),
        #     'password': forms.TextInput(attrs={'class': 'reg'}),
        #     'password2': forms.TextInput(attrs={'class': 'reg'}),
        #     'email': forms.EmailInput(attrs={'class': 'reg'}),
        # }

    def clean_password2(self):
        pswd, pswd2 = self.cleaned_data['password'], self.cleaned_data['password2']
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают!')

        digits = re.search('[0-9]', pswd)
        uppercase = re.search('[A-Z]', pswd)
        lowercase = re.search('[a-z]', pswd)
        has_special = re.compile("|".join(map(re.escape, string.punctuation))).search(pswd)
        if len(pswd) < 8 or not digits or not uppercase or not lowercase or not has_special:
            raise forms.ValidationError('Пароль должен состоять из 8 и более символов, '
                                        'а также содержать специальные символы и буквы верхнего регистра!')
        return pswd

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Такой e-mail уже существует!')
        return email

    def clean_login(self):
        login = self.cleaned_data['login']
        if get_user_model().objects.filter(login=login).exists():
            raise forms.ValidationError('Пользователь с таким логином уже существует!')
        return login


class LoginForm(forms.Form):
    username = forms.CharField(label='Имя пользователя',
                               widget=forms.TextInput(attrs={'placeholder': 'Введите имя пользователя',
                                                             'class': 'form-control',
                                                             'name': 'username'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль',
                                                                                 'class': 'form-control',
                                                                                 'name': 'password'}))


class AddBookForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(AddBookForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    lang = Language.objects.all()
    lang_choices = []
    for i in lang:
        lang_choices.append((i.name, i.name.capitalize()))
    genres = Genre.objects.all()
    genre_choices = []
    for i in genres:
        genre_choices.append((i.name, i.name.capitalize()))
    title = forms.CharField(label='Название')
    author = forms.CharField(label='Автор')
    description = forms.CharField(label='Описание', widget=forms.Textarea())
    print = forms.CharField(label='Издательство')
    pub_date = forms.DateField(label='Год выпуска')
    genre = forms.MultipleChoiceField(label='Жанр', choices=tuple(genre_choices))
    language = forms.MultipleChoiceField(label='Языки', choices=tuple(lang_choices))
    ISBN = forms.RegexField(label='ISBN', regex=r'\d{3}-\d{1}-\d{3}-\d{5}-\d{5}')


class edit_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(edit_form, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    photo = forms.ImageField(label='Фото профиля', required=False)

    city = forms.CharField(label='Город', required=False)
    birth = forms.DateField(label='Дата рождения', required=False)
    bio = forms.CharField(label='О себе', required=False, widget=forms.Textarea)

    class Meta:
        model = Profile

        fields = ['city', 'birth', 'bio', 'photo']


class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')

    class Meta:
        model = User
        fields = ['last_name', 'first_name']


class ChangePasswordForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    old_password = forms.CharField(label='Старый пароль', widget=forms.PasswordInput(attrs=
    {
        'placeholder': 'Введите старый пароль'}))
    new_password = forms.CharField(label='Новый пароль', widget=forms.PasswordInput(attrs=
    {
        'placeholder': 'Введите новый пароль'}))
    new_password_confirm = forms.CharField(label='Подтверждение', widget=forms.PasswordInput(attrs=
    {
        'placeholder': 'Подтвердите пароль'}))

    class Meta:
        model = User

        fields = ['old_password', 'new_password']

    # def clean_old_password(self):
    #     old_password = self.cleaned_data['old_password']
    #     if old_password == self.user.password:
    #         return old_password
    #     else:
    #         raise forms.ValidationError('Введеный пароль неверен.!')

    def clean_password2(self):
        pswd, pswd2 = self.cleaned_data['new_password'], self.cleaned_data['new_password_confirm']

        if pswd != pswd2:
            raise forms.ValidationError('Пароли не совпадают!')

        digits = re.search('[0-9]', pswd)
        uppercase = re.search('[A-Z]', pswd)
        lowercase = re.search('[a-z]', pswd)
        has_special = re.compile("|".join(map(re.escape, string.punctuation))).search(pswd)
        if len(pswd) < 8 or not digits or not uppercase or not lowercase or not has_special:
            raise forms.ValidationError('Пароль должен состоять из 8 и более символов, '
                                        'а также содержать специальные символы и буквы верхнего регистра!')
        return pswd


# def clean_pass(obj):
#     pswd = obj.cleaned_data['password']
#     if not get_user_model().objects.filter(password=pswd).exists():
#         raise forms.ValidationError('Введеный пароль неверен.')
#     return pswd
# def clean_pass(pswd):
#     if check_password(pswd,use)
#     if not get_user_model().objects.filter(password=pswd).exists():
#         raise forms.ValidationError('Введеный пароль неверен.')
#     return pswd


class ChangeLoginForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ChangeLoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput())
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs=
    {
        'placeholder': 'Введите пароль для подтверждения'}))

    class Meta:
        model = User
        fields = ('username', 'password')

    def clean_pass(self):
        pswd = self.cleaned_data['password']
        if check_password(pswd, self.user.password):
            return pswd
        else:
            raise forms.ValidationError('Введеный пароль неверен.!!!')

    def clean_login(self):
        username = self.cleaned_data['username']
        if self.user and self.user.username == username:
            return username

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким именем уже !!!существует.')
        return username


class ChangeEmailForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ChangeEmailForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    email = forms.EmailField(label='Электронная почта')

    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs=
    {
        'placeholder': 'Введите пароль для подтверждения'}))

    class Meta:
        model = get_user_model()
        fields = ('email', 'password')

    def clean_email(self):
        email = self.cleaned_data['email']
        if self.user and self.user.email == email:
            return email

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с такой электронной почтой уже существует')
        return email
