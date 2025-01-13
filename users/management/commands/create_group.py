from django.core.management import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    """Команда создания готовых групп"""

    def handle(self, *args, **options):
        group_name = str(input('Название группы: '))
        group, created = Group.objects.get_or_create(name=group_name)

        if created:
            print(f"Группа '{group_name}' успешно создана.")
        else:
            print(f"Группа '{group_name}' уже существует.")
