from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail

from users.models import User


class SchoolAdminCreationForm(forms.Form):
    """Форма регистрации в системе - создание школьного администратора и школы"""

    name = forms.CharField(max_length=30, label="Имя")
    surname = forms.CharField(max_length=30, label="Фамилия")
    patronymic = forms.CharField(max_length=30, label="Отчество")
    email = forms.EmailField(label="Адрес электронной почты")
    password = forms.CharField(widget=forms.PasswordInput(), label="Пароль")
    password_again = forms.CharField(widget=forms.PasswordInput(), label="Пароль еще раз")

    region = forms.CharField(max_length=100, label="Регион")
    city = forms.CharField(max_length=100, label="Город")
    school = forms.CharField(max_length=100, label="Школа")

    def clean(self):
        password = self.cleaned_data["password"]
        password_again = self.cleaned_data["password_again"]
        if password != password_again:
            raise forms.ValidationError("Пароли не совпадают")

    def clean_email(self):
        try:
            user = User.objects.get(email=self.cleaned_data["email"])
            if user:
                raise forms.ValidationError("Пользователь с такой почтой уже существует")
        except User.DoesNotExist:
            return self.cleaned_data["email"]

    def send_registration_mail(self):
        email = self.cleaned_data["email"]
        send_mail(
            "Регистрация на DiarySpace",
            "Спасибо, что выбрали DiarySpace!\nОжидайте ответа от нас в течение суток.",
            "noreply@diaryspace.com",
            [email],
            fail_silently=False
        )
