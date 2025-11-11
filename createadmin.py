from django.contrib.auth import get_user_model
from django.core.management import execute_from_command_line
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog.settings")
import django
django.setup()

User = get_user_model()

username = "DILNAVAZ"
email = "dnavaz538@gmail.com"
password = "DILnavaz@123"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print("✅ Superuser created successfully!")
else:
    print("ℹ️ Superuser already exists.")
