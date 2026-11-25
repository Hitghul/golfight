from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create the default admin account if it does not exist."

    def handle(self, *args, **options):
        users = get_user_model().objects
        if not users.filter(username="admin").exists():
            users.create_superuser(username="admin", password="projetinfo1A")
