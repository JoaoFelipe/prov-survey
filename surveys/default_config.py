# -*- coding: utf-8 -*-
# The default_config module automatically gets imported by Appconfig, if it
# exists. See https://pypi.python.org/pypi/flask-appconfig for details.

# Note: Don't *ever* do this in a real app. A secret key should not have a
#       default, rather the app should fail if it is missing. For the sample
#       application, one is provided for convenience.
import os
basedir = os.path.abspath(os.path.dirname(__file__))

def env(value, other=None):
    if value in os.environ:
        return os.environ[value]
    return other

SECRET_KEY = env('SURVEY_SECRET', 'secret?')

SQLALCHEMY_DATABASE_URI = env(
    'DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'app.db')
)
SQLALCHEMY_TRACK_MODIFICATIONS = False

MAIL_SERVER = env('EMAIL_SERVER', 'smtp.gmail.com')
MAIL_PORT = int(env('EMAIL_PORT', 465)) # 587?
MAIL_USE_SSL = bool(int(env('EMAIL_USE_SSL', 1)))
MAIL_USERNAME = env('EMAIL_USERNAME')
MAIL_PASSWORD = env('EMAIL_PASSWORD')

GITHUB = env('GITHUB', '~/script-analysis')

gmail = 'gmail.com'
newcastle = 'newcastle.ac.uk'
CONTACTS = {
    'joao': ('joaofelipenp', gmail),
    'wellington': ('wmoliveira1', gmail),
    'leo': ('leomurta', gmail),
    'vanessa': ('vanessa.braganholo', gmail),
    'daniel': ('danielcmo', gmail),
    'paolo': ('paolo.missier', newcastle),
}


LANGUAGES = {
    'en': u'English',
    'ptbr': u'Português',
}

LANGUAGES_LOCALE = {
    'en': 'en',
    'ptbr': 'pt_BR',
}

DEBUG = bool(int(env('SURVEY_DEBUG', 0)))
