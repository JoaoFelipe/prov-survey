# -*- coding: utf-8 -*-
# The default_config module automatically gets imported by Appconfig, if it
# exists. See https://pypi.python.org/pypi/flask-appconfig for details.

# Note: Don't *ever* do this in a real app. A secret key should not have a
#       default, rather the app should fail if it is missing. For the sample
#       application, one is provided for convenience.
import os
basedir = os.path.abspath(os.path.dirname(__file__))


SECRET_KEY = 'secret?'

SQLALCHEMY_DATABASE_URI = (
	os.environ['DATABASE_URL'] if 'DATABASE_URL' in os.environ
	else 'sqlite:///' + os.path.join(basedir, 'app.db')
)
SQLALCHEMY_TRACK_MODIFICATIONS = False


LANGUAGES = {
    'en': u'English',
    'ptbr': u'Português',
}

LANGUAGES_LOCALE = {
    'en': 'en',
    'ptbr': 'pt_BR',
}