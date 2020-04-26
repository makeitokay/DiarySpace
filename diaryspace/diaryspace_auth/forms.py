from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.mail import send_mail

from diaryspace_auth.models import User


class UserCreateForm(forms.Form):
    name = forms.CharField(max_length=30, label="Имя")
    surname = forms.CharField(max_length=30, label="Фамилия")
    patronymic = forms.CharField(max_length=30, label="Отчество")
    email = forms.EmailField(label="Адрес электронной почты")

    def __init__(self, *args, **kwargs):
        self.school_id = None
        if "school_id" in kwargs:
            self.school_id = kwargs.pop("school_id")
        super().__init__(*args, **kwargs)

    def clean_email(self):
        try:
            user = User.objects.get(email=self.cleaned_data["email"])
            if user:
                raise forms.ValidationError(
                    "Пользователь с такой почтой уже существует"
                )
        except User.DoesNotExist:
            return self.cleaned_data["email"]


class SchoolAdminCreationForm(UserCreateForm):
    """Форма регистрации в системе - создание школьного администратора и школы"""

    password = forms.CharField(widget=forms.PasswordInput(), label="Пароль")
    password_again = forms.CharField(
        widget=forms.PasswordInput(), label="Пароль еще раз"
    )

    region = forms.CharField(max_length=100, label="Регион")
    city = forms.CharField(max_length=100, label="Город")
    school = forms.CharField(max_length=100, label="Школа")

    def clean(self):
        password = self.cleaned_data["password"]
        validate_password(password)
        password_again = self.cleaned_data["password_again"]
        if password != password_again:
            raise forms.ValidationError("Пароли не совпадают")

    def send_registration_mail(self):
        email = self.cleaned_data["email"]
        send_mail(
            "Регистрация на DiarySpace",
            "Спасибо, что выбрали DiarySpace!\nОжидайте ответа от нас в течение суток.",
            "noreply@diaryspace.com",
            [email],
            fail_silently=False,
        )
