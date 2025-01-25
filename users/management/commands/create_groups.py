from django.core.management import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    """Команда создания готовых групп"""

    def handle(self, *args, **options):
        group1, created1 = Group.objects.get_or_create(name="promotioner")
        group2, created2 = Group.objects.get_or_create(name="waiter")
        group3, created3 = Group.objects.get_or_create(name="contentmanager")
        group4, created4 = Group.objects.get_or_create(name="observer")

        for group, created in {group1: created1, group2: created2, group3: created3, group4: created4}.items():
            if created:
                print(f"Группа '{group.name}' успешно создана.")
            else:
                print(f"Группа '{group.name}' уже существует.")