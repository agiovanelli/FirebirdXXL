import os
from web_project.settings import BASE_DIR


STATIC_URL = '/static/'

# Questo dovrebbe già essere presente se stai usando il comando collectstatic
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
