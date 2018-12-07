from django.contrib.auth.hashers import make_password
from django.db.models.signals import post_migrate
from .models import UserProfile

def init_db(sender, **kwargs):
    if not UserProfile.objects.exists():
        UserProfile.objects.create(username='admin',nickname='admin',password=make_password('admin'),is_superuser=True,is_staff=True)

post_migrate.connect(init_db)