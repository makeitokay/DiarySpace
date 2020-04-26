from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand

from diaryspace_auth import groups


class Command(BaseCommand):
    help = "Creates groups of users (School admin, Teacher, Student, Parent) and permissions for them"

    _PERMISSIONS = {
        groups.SCHOOL_ADMIN: {
            "lesson": ["view", "change", "add", "delete"],
            "mark": ["view", "change", "add", "delete"],
            "announcement": ["view", "change", "add", "delete"],
            "schedule": ["view", "change", "add", "delete"],
            "grade": ["view", "change", "add", "delete"],
            "callschedule": ["view", "change", "add", "delete"],
            "school": ["view", "change"],
            "subject": ["view", "change", "add", "delete"],
            "parent": ["view", "change", "add", "delete"],
            "student": ["view", "change", "add", "delete"],
            "teacher": ["view", "change", "add", "delete"],
        },
        groups.TEACHER: {
            "lesson": ["view", "change", "add"],
            "mark": ["view", "change", "add"],
            "announcement": ["view", "change", "add"],
        },
        groups.PARENT: {
            "diary": ["view"],
            "reports": ["view"],
            "announcement": ["view"],
        },
        groups.STUDENT: {
            "diary": ["view"],
            "reports": ["view"],
            "announcement": ["view"],
        },
    }

    # TODO: возможно, использовать встроенный в Django перевод?
    _PERMISSION_INTO_RUSSIAN = {
        "can": "может",
        "view": "смотреть",
        "change": "изменять",
        "add": "добавлять",
        "delete": "удалять",
        "lesson": "уроки",
        "mark": "оценки",
        "announcement": "объявления",
        "schedule": "расписание",
        "grade": "классы",
        "call schedule": "расписание звонков",
        "school": "информацию о школе",
        "subject": "предметы",
        "parent": "родителей",
        "student": "учеников",
        "teacher": "учителей",
        "student diary": "дневник",
        "student reports": "отчёты",
    }

    def handle(self, *args, **options):
        for group_name, permissions in self._PERMISSIONS.items():
            group, created = Group.objects.get_or_create(name=group_name)
            if created is True:
                print(f"Group `{group_name}` ✓")
            for entity in permissions:
                for permission_name in permissions[entity]:
                    codename = f"{permission_name}_{entity}"
                    try:
                        permission = Permission.objects.get(codename=codename)
                    except Permission.DoesNotExist:
                        raise ImproperlyConfigured(
                            f"Permission `{codename}` not found."
                            " Maybe, you should run `python manage.py makemigrations && python manage.py migrate`"
                            " before using `databaseinit`?"
                        )
                    name = permission.name.lower()
                    if "может" not in name:
                        words = name.split(permission_name)
                        words.insert(1, permission_name)
                        permission.name = " ".join(
                            [self._PERMISSION_INTO_RUSSIAN[w.strip()] for w in words]
                        ).capitalize()
                        permission.save()
                    if group.permissions.filter(codename=codename).exists():
                        continue
                    print(f"{group_name}: `{codename}` ✓")
                    group.permissions.add(permission)
