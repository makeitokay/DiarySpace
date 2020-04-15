from django.conf import settings
from django.db import models


class Lesson(models.Model):
    class Meta:
        permissions = (
            ('view_diary', 'Can view student diary'),
        )

    school = models.ForeignKey('schools.School', on_delete=models.CASCADE, related_name='lessons')
    subject = models.ForeignKey('schools.Schedule', on_delete=models.SET_NULL, null=True, related_name='lessons')
    grade = models.ForeignKey('schools.Grade', on_delete=models.SET_NULL, null=True, related_name='lessons')

    date = models.DateField(verbose_name='дата урока')
    theme = models.TextField(verbose_name='тема')
    homework = models.TextField(verbose_name='домашнее задание')


class Mark(models.Model):
    class Meta:
        permissions = (
            ('view_reports', 'Can view student reports'),
        )

    school = models.ForeignKey('schools.School', on_delete=models.CASCADE, related_name='marks')
    lesson = models.ForeignKey('Lesson', on_delete=models.SET_NULL, null=True, related_name='marks')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='marks')

    ATTENDANCE_CHOICES = (
        ('УП', 'Уважительная причина'),
        ('Б', 'Болеет'),
        ('ОП', 'Опоздал'),
        ('ОТ', 'Отсутствует')
    )

    mark = models.PositiveSmallIntegerField(verbose_name='оценка')
    attendance = models.CharField(max_length=2, null=True, verbose_name='посещаемость', choices=ATTENDANCE_CHOICES)
