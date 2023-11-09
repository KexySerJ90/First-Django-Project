import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="Логин/E-mail", widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    remember_me = forms.BooleanField(label="Запомнить меня", required=False)


    class Meta:
        model=get_user_model()
        fields=['username', 'password','remember_me']

    def clean_remember_me(self):
        remember_me = self.cleaned_data.get('remember_me')
        if remember_me:
            self.request.session.set_expiry(86400*365)
        else:
            self.request.session.set_expiry(86400)


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label="*Логин", widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label="*Пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label="*Повтор пароля", widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model= get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        labels={
            'email': "*E-mail",
            "first_name":"Имя",
            "last_name":"Фамилия"
        }
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
        }


    def clean_email(self):
        email=self.cleaned_data.get('email')
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Email уже существует")
        return email


class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.CharField(disabled=True, required=False, label='E-mail', widget=forms.TextInput(attrs={'class': 'form-input'}))
    this_year=datetime.date.today().year
    date_birth=forms.DateTimeField(label="Дата рождения",widget=forms.SelectDateWidget(years=tuple(range(this_year-100,this_year-5))))


    class Meta:
        model = get_user_model()
        fields = ['photo','username', 'email','date_birth', 'first_name', 'last_name']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
        }



class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Старый пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password1 = forms.CharField(label="Новый пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput(attrs={'class': 'form-input'}))


