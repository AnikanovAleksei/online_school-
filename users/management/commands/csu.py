from django.core.management import BaseCommand

from users.models import SchoolUser


class Command(BaseCommand):
    def handle(self, *args, **options):
        school_user = SchoolUser.objects.create(email='admin@mail.ru')
        school_user.is_staff = True
        school_user.is_active = True
        school_user.is_superuser = True
        school_user.set_password('12345')
        school_user.save()
