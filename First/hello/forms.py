from django import forms
import re


# class UserForm(forms.Form):
#     def __init__(self, *args, **kwargs):
#         super(UserForm, self).__init__(*args, **kwargs)
#         for visible in self.visible_fields():
#             visible.field.widget.attrs['class'] = 'form-user'
#
#     CHOICES = (('Python', 'Python'), ('JavaScript', 'JavaScript'), ('C++', 'C++'), ('Java', 'Java'),)
#     name = forms.CharField(min_length=5, max_length=15)
#     age = forms.IntegerField(min_value=1, max_value=99)
#     # langs = forms.ChoiceField(choices=('Python', 'JavaScript', 'C++', 'Java',))
#     langs = forms.ChoiceField(choices=CHOICES)


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            # visible.field.widget.attrs['class'] = 'form-login'
            match = re.search(r'name="\w+"', str(visible))
            name_widget = re.sub(r'name=|"', '', match[0])
            visible.field.widget.attrs['placeholder'] = f'Enter {name_widget}'

    login = forms.CharField(min_length=5, max_length=15, label='')
    password = forms.CharField(max_length=50, widget=forms.PasswordInput, label='')


class RegForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(RegForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            # visible.field.widget.attrs['class'] = 'form-login'
            match = re.search(r'name="\w+"', str(visible))
            name_widget = re.sub(r'name=|"', '', match[0])
            visible.field.widget.attrs['placeholder'] = f'Enter {name_widget}'

    email = forms.EmailField(required=True, label='', )
    login = forms.CharField(min_length=5, max_length=15, required=True, label='',)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput, required=True, label='',)
