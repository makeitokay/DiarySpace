from django.db import models

from diaryspace_auth.models import User
from schools.models import Grade, Subject


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
