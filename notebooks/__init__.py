"""
> cd notebooks
> python ../manage.py shell_plus --notebook

>>> from notebooks import init
>>> init()
"""

import os
import sys
import django


def init():
    sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tdxStock.settings')
    django.setup()
