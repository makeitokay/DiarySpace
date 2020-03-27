from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
    Group,
)
from schools.models import School, Grade, Subject


class UserManager(BaseUserManager):
    def create_user(
        self, email, password, school_id=None, name="", surname="", patronymic=""
    ):
        if not email:
            raise ValueError("Email is a required field")

        user = self.model(
            email=self.normalize_email(email),
            school_id=school_id,
            name=name,
            surname=surname,
            patronymic=patronymic,
        )
        user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password,)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def create_school_admin(
        self, email, password, name, surname, patronymic, school_id
    ):
        user = self.create_user(email, password, school_id, name, surname, patronymic)
        group = Group.objects.get(name="SchoolAdmin")
        user.groups.add(group)
        user.save(using=self._db)

        SchoolAdmin.objects.create(user=user)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="email address", max_length=255, unique=True)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    patronymic = models.CharField(max_length=30)

    school = models.ForeignKey(
        School, on_delete=models.CASCADE, related_name="users", null=True, default=None
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

    @property
    def role(self):
        if self.groups.exists():
            return self.groups.first().name
        return None


class ApprovedSchoolAdminManager(models.Manager):
    def get_approved(self):
        return super().get_queryset().filter(request_approved=True)


class SchoolAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    request_approved = models.BooleanField(default=False)

    objects = ApprovedSchoolAdminManager()

    def __str__(self):
        return str(self.user)


class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    grade = models.ForeignKey(
        Grade, on_delete=models.SET_NULL, null=True, related_name="students"
    )
    parent = models.ForeignKey(
        Parent, on_delete=models.SET_NULL, null=True, related_name="children"
    )

    def __str__(self):
        return self.user.email


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    homeroom_grade = models.OneToOneField(
        Grade, on_delete=models.SET_NULL, null=True, related_name="homeroom_teacher"
    )
    subjects = models.ManyToManyField(Subject)

    def __str__(self):
        return self.user.email
