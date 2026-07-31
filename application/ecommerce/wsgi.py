
import os
from django.core.wsgi import get_wsgi_application
# Hide Gunicorn server header for proxy compatibility
import gunicorn
gunicorn.SERVER = ''

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
application = get_wsgi_application()
