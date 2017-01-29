"""Helpers functions to build a survey"""
from copy import copy
from functools import wraps

from flask import session, render_template, redirect, url_for, flash
from flask_babel import gettext
from flask_nav.elements import View

from .db import db, Answer

def save_answer(number, data=None):
    data = data if data is not None else session['s_{}_a'.format(number)]
    uid = session['s_uid']
    Answer.query.filter_by(uid=uid, question=number).delete()
    for key, value in data.items():
        if value:
            db.session.add(Answer(uid, number, key, str(value)))
    db.session.commit()

def last(order):
    """Return last visited"""
    for elements in reversed(order):
        if not isinstance(elements, tuple):
            elements = (elements,)
        for element in elements:
            number = element.lower()
            sid = 's_{}'.format(number)
            if sid in session:
                return tuple(x.lower() for x in elements)
    return ('index',)


def erase(numbers):
    """Remove question from NavBar"""
    if isinstance(numbers, str):
        numbers = [numbers]
    uid = session['s_uid']
    for number in numbers:
        Answer.query.filter_by(uid=uid, question=number).delete()
        sid = 's_{}'.format(number)
        sid_ans = sid + '_a'
        if sid in session:
            del session[sid]
        if sid_ans in session:
            del session[sid_ans]

    db.session.commit()


def question(form, title):
    """Render question template"""
    return render_template('question.html', form=form, title=title)


def question_url(number=None, lang=None):
    """Url for question"""
    number = number or (session['s_url'] if 's_url' in session else 'index')
    lang = lang or (session['s_lang'] if 's_lang' in session else 'en')
    return url_for(".question", lang=lang, number=number)


def goto(number):
    """Redirect to another question"""
    if isinstance(number, tuple):
        number = number[-1]
    if not isinstance(number, str):
        number = number()
    return redirect(question_url(number))


def local_view(text, number=None, lang=None):
    """NavBar view for questions"""
    number = number or (session['s_url'] if 's_url' in session else 'index')
    lang = lang or (session['s_lang'] if 's_lang' in session else 'en')
    return View(text, '.question', lang=lang, number=number)


def question_form(number, next_question, form_class, title, alternative=None):
    """Process GET and POST of a question form"""
    alternative = alternative or (lambda form: False)
    answer = 's_{}_a'.format(number)
    form = form_class(**session.get(answer, {}))
    if alternative(form) or form.validate_on_submit():
        session[answer] = copy(form.data)
        del session[answer]['submit']
        del session[answer]['csrf_token']
        save_answer(number)
        # ToDo: save
        return goto(next_question)
    return question(form, title)


def radio_question(number, next_question, form_class, title):
    """Process GET and POST of a radio question form. Support empty question"""
    return question_form(
        number, next_question, form_class, title,
        lambda form: (form.submit.data and form.options.data == 'None')
    )


def answer(number):
    """Get answer"""
    return session.get('s_{}_a'.format(number), {})


def option(number, default='no'):
    """Get answer from Radio Question"""
    return answer(number).get('options', default)


def survey_started(func):
    """Check if survey has started"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        """Check if survey has started"""
        if 's_uid' not in session:
            flash(gettext("Invalid Session. Restarting"))
            return goto('index')
        return func(*args, **kwargs)
    return wrapper


def to_tuple(element):
    if isinstance(element, tuple):
        return element
    return (element,)


def require(numbers):
    """Require previous question"""
    if isinstance(numbers, str):
        numbers = [numbers]
    def decorator(func):
        """Check if survey has started"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            """Check if survey has started"""
            go_back = last(numbers)
            if to_tuple(numbers[-1]) != go_back:
                return goto(go_back if go_back != ('index',) else numbers[0])
            return func(*args, **kwargs)
        return wrapper
    return decorator


def set_navbar(minutes):
    """Set remaining minutes in the navbar"""
    def decorator(func):
        """Actual decorator"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            """Set lang, url, accessed page and remaining minutes"""
            lang = session['s_lang']
            session['s_lang'] = lang
            session['s_url'] = func.__name__
            session['s_' + func.__name__] = True
            if minutes == 1:
                session['s_minutes'] = gettext("~1 minute remaining")
            elif isinstance(minutes, int):
                session['s_minutes'] = gettext(
                    "~%(minutes)s minutes remaining", minutes=minutes)
            else:
                session['s_minutes'] = minutes
            return func(*args, **kwargs)

        return wrapper
    return decorator

def survey_question(numbers, minutes):
    """Condenses survey_started, require, and set_navbar"""
    def decorator(func):
        """Condenses survey_started, require, and set_navbar"""
        return survey_started(require(numbers)(set_navbar(minutes)(func)))
    return decorator
