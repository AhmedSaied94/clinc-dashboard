# +++++++++++ DJANGO +++++++++++
# To use your own django app use code like this:
import os
import sys

# Add your project directory to the sys.path
path = '/home/AhmedSaied94/clinc_dashboard'
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variable to tell Django to use production settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'clinic_dashboard.settings.production'

# Activate your virtual environment
# Note: Replace 'venv' with your actual virtual environment name
# PythonAnywhere will show you the exact path when you create the web app
# virtualenv = '/home/AhmedSaied94/.virtualenvs/clinc_dashboard/bin/activate_this.py'
# with open(virtualenv) as f:
#     exec(f.read(), {'__file__': virtualenv})

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
