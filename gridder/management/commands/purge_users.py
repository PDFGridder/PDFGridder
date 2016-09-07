import datetime
from django.core.management.base import NoArgsCommand
from django.contrib.auth.models import User


class Command(NoArgsCommand):
    def handle(self, *args, **options):
        a_year_ago = datetime.datetime.now() - datetime.timedelta(days=365)
        User.objects.filter(last_login__lt=a_year_ago).delete()
