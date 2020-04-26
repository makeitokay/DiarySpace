from django.conf import settings
from django.db import models


class Parent(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)


class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    grade = models.ForeignKey(
        "schools.Grade", on_delete=models.SET_NULL, null=True, related_name="students"
    )
    parent = models.ForeignKey(
        "users.Parent", on_delete=models.SET_NULL, null=True, related_name="children"
    )

    def __str__(self):
        return str(self.user)


class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    homeroom_grade = models.OneToOneField(
        "schools.Grade",
        on_delete=models.SET_NULL,
        null=True,
        related_name="homeroom_teacher",
    )
    subjects = models.ManyToManyField("schools.Subject")

    def __str__(self):
        return str(self.user)
