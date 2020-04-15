from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
    Group,
)
from django.utils.functional import cached_property

from schools.models import School, Grade, Subject
from diaryspace_auth import groups


class UserManager(BaseUserManager):
    def create_user(
        self,
        email=None,
        password=None,
        school_id=None,
        name="",
        surname="",
        patronymic="",
        is_active=True,
    ):
        if email is None:
            raise ValueError("Email is a required field")
        if password is None:
            raise ValueError("Password is a required field")

        user = self.model(
            email=self.normalize_email(email),
            school_id=school_id,
            name=name,
            surname=surname,
            patronymic=patronymic,
            is_active=is_active,
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email=email, password=password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

    def create_school_admin(self, **kwargs):
        user = self.create_user(**kwargs, is_active=False)
        group = Group.objects.get(name=groups.SCHOOL_ADMIN)
        user.groups.add(group)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name="электронный адрес", max_length=255, unique=True
    )
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    patronymic = models.CharField(max_length=30)

    school = models.ForeignKey(
        'schools.School', on_delete=models.CASCADE, related_name="users", null=True, default=None
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin

    @cached_property
    def group(self):
        return self.groups.first()
