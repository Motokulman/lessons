# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, '/home/z/z25945zw/inserty/lessons')
sys.path.insert(1, '/home/z/z25945zw/.local/lib/python3.7/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'lessons.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()