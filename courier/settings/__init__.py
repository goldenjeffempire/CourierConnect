import os

env = os.getenv('DJANGO_SETTINGS_MODULE', 'courier.settings.dev').split('.')[-1]

if env == 'prod':
    from .prod import *
else:
    from .dev import *
