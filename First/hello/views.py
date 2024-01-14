from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.template.response import TemplateResponse
from .forms import *
from .models import *
from django.db import connection
from datetime import datetime

# class LoginUser(DataMixin, LoginView):
#     form_class = AuthenticationForm
#     template_name = 'templates/index.html'
#
#     def get_context_data(self, object_list=None ,**kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context(title='Авторизация')
#         return dict(list(context.items()) + list(c_def.items()))
data_db = UserModel.objects.all()


def index(request):
    Log_Form = LoginForm()
    if request.method == 'POST':
        Log_Form = LoginForm(request.POST)
        if Log_Form.is_valid():
            login = Log_Form.cleaned_data['login']
            passwd = Log_Form.cleaned_data['password']
            is_exist = None
            is_exist = UserModel.objects.filter(login=login, password=passwd)
            print(is_exist)
            if is_exist:
                return render(request, template_name="main.html", context={'name': login})
            else:
                print('Не существует!')

    return render(request, "index.html", context={"form": Log_Form})


def registration(request):
    reg_form = RegForm()
    if request.method == 'POST':
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            email = reg_form.cleaned_data['email']
            login = reg_form.cleaned_data['login']
            passwd = reg_form.cleaned_data['password']
            user = UserModel(email=email, login=login, password=passwd)
            try:
                user.save()
            except Exception as e:
                print(f"Invalid data with error {e}")
                return render(request, 'registration.html', context={"form": reg_form})
            return redirect('login')
    return render(request, 'registration.html', context={"form": reg_form})


def test(request):
    # with connection.cursor() as cursor:
    #     cursor.execute("SELECT * FROM hello_UserModel")
    #     data_db = cursor.fetchall()
    data = {'data_db': UserModel.objects.all(), 'selected': 0, }
    return render(request, 'test.html', context=data)
