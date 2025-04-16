# accounts/context_processors.py
from django.contrib.auth.models import Group

def admin_group(request):
    if request.user.is_authenticated:
        is_admin = request.user.groups.filter(name='admin').exists()
    else:
        is_admin = False
    return {'is_admin': is_admin}

