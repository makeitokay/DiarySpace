from django.db import models

from diaryspace.settings import AUTH_USER_MODEL


class School(models.Model):
    region = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    school = models.CharField(max_length=100)

    def __str__(self):
        return ", ".join([self.region, self.city, self.school])


class Grade(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="grades")
    number = models.PositiveSmallIntegerField()
    letter = models.CharField(max_length=1)


class Subject(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="subjects")
    name = models.CharField(max_length=50)


class Schedule(models.Model):
    DAYS_CHOICES = (
        (1, "Понедельник"),
        (2, "Вторник"),
        (3, "Среда"),
        (4, "Четверг"),
        (5, "Пятница"),
        (6, "Суббота"),
        (7, "Воскресенье")
    )

    day = models.IntegerField(choices=DAYS_CHOICES)
    subject_number = models.PositiveSmallIntegerField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="schedule")
    teacher = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="schedule")
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name="schedule")
