"""Navbar and routes"""

from flask import Blueprint, session, request, current_app
from flask_babel import lazy_gettext

from . import survey
from .babel import babel
from .helper import local_view, last, goto, answer
from .nav import nav, ExtendedNavbar

GET_POST = ('GET', 'POST')
frontend = Blueprint('frontend', __name__)


def frontend_top():
    """Calculate Navbar"""
    languages = current_app.config['LANGUAGES']
    args = []
    if 's_index' in session:
        args.append(local_view(lazy_gettext('Start2'), 'index'))
    for element in survey.ORDER:
        lele = element.lower()
        if 's_' + lele in session:
            view = local_view(element, lele)
            ans = answer(lele)
            if lele != session['s_url']:
                if 'options' in ans and ans['options'] == 'None':
                    view.classes = ["unanswered"]
                elif len(ans) == sum(1 for x in ans.values() if not x):
                    view.classes = ["unanswered"]
            args.append(view)
    language_items = [local_view(v, lang=k) for k, v in languages.items()
                      if k != session['s_lang']]

    return ExtendedNavbar(
        title=local_view(session['s_minutes']),
        items=args, right_items=language_items
    )

nav.register_element('frontend_top', frontend_top)

@babel.localeselector
def get_locale():
    """Select locale according to session['s_lang']"""
    locale = current_app.config['LANGUAGES_LOCALE']
    # if a user is logged in, use the locale from the user settings
    if 's_lang' in session:
        return locale[session['s_lang']]
    return request.accept_languages.best_match(locale.values())


@frontend.route('/')
def root():
    """Redirect to ptbr"""
    return goto('index')


@frontend.route('/<lang>/', defaults={'number': 'index'}, methods=GET_POST)
@frontend.route('/<lang>/<number>/', methods=GET_POST)
def question(lang, number):
    """Survey question routes"""
    languages = current_app.config['LANGUAGES']
    session['s_lang'] = lang if lang in languages else 'en'
    if hasattr(survey, number):
        return getattr(survey, number)()
    return goto(last(survey.ORDER))
