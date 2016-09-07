import os
import sys
import site
from django.core.wsgi import get_wsgi_application

import dotenv

dotenv.read_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

site.addsitedir('/var/www/pdfgridder/lib/python2.7/site-packages')
sys.path.append('/var/www/pdfgridder')
sys.path.append('/var/www/pdfgridder/pdfgridder')

os.environ['PATH'] += ':/var/lib/gems/1.8/bin'
os.environ['DJANGO_SETTINGS_MODULE'] = 'pdfgridder.settings_production'

application = get_wsgi_application()
