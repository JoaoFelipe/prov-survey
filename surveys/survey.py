"""Survey questions"""
# pylint: disable=invalid-name
# pylint: disable=line-too-long

import os
import binascii
from collections import OrderedDict

from flask import session, render_template
from flask_babel import gettext, lazy_gettext

from itertools import chain

from .db import db, Answer

from .helper import erase, goto, question_form, radio_question, last, answer
from .helper import option, set_navbar, survey_question, save_answer

from .forms import StartForm, NextForm
from .forms import Education, ExperimentCount, Domains, Experience, Situations
from .forms import Tools, Preference, PreferenceReasons
from .forms import Integration, Likelyhood
from .forms import Analysis, AnalysisReasons, AnalysisTools
from .forms import EmailForm, YesNo

FORMS = OrderedDict([
    ('p1', Education),
    ('p2', ExperimentCount),
    ('p3', Domains),
    ('p4', Experience),
    ('p5', Situations),
    ('t1', Tools),
    ('t2', Preference),
    ('t3', PreferenceReasons),
    ('i1', Integration),
    ('i2', Likelyhood),
    ('a1', Analysis),
    ('a2', AnalysisReasons),
    ('a3', AnalysisTools),
    ('a4', YesNo),
    ('a5', YesNo),
    ('c1', YesNo),
    ('c2', YesNo),
    ('c3', EmailForm),
])

ORDER = [x.upper() for x in FORMS.keys()] + ['finish']


def form(number, next_question, title, options=None):
    """Question Form based on Form type"""
    form_class = FORMS[number]
    question_function = (
        question_form if form_class._mode != 'radio' else radio_question
    )
    return question_function(
        number, next_question, form_class, title,
        options=options
    )


@set_navbar(9)
def index():
    """First page"""
    lang = session['s_lang']
    form = (NextForm if 's_uid' in session else StartForm)()
    if form.validate_on_submit():
        if form.submit.data:
            if 's_uid' in session:
                save_answer('finish', {'submit': 'restart'})
            session.clear()
            session['s_lang'] = lang
            session['s_index'] = True
            session['s_uid'] = binascii.hexlify(os.urandom(24))
            save_answer('index', {'submit': 'yes'})
            # ToDo: save
        session['s_p1'] = True
        return goto('p1')
    return render_template('index.html', form=form)


@survey_question('index', 8)
def p1():
    """Q1/P1"""
    title = gettext('What is your educational level?')
    return form('p1', 'p2', title)


@survey_question('p1', 8)
def p2():
    """Q2/P2"""
    title = gettext('How many scientific experiments have you ever performed on computational environments?')
    return form('p2', (lambda: 'p3' if option('p2') != '0' else 'finish'), title)


@survey_question('p2', 7)
def p3():
    """Q3/P3"""
    title = gettext('What are your scientific domains? (check all that apply)')
    return form('p3', 'p4', title)


@survey_question('p3', 7)
def p4():
    """Q4/P4"""
    title = gettext('How much experience do you have in running scientific experiments on computational environments?')
    return form('p4', 'p5', title)


@survey_question('p4', 6)
def p5():
    """Q5/P5"""
    title = gettext('In which roles have you performed computational experiments? (check all that apply)')
    return form('p5', 't1', title)


def t1_answers():
    ans = answer('t1')
    items = [
        (k, getattr(Tools, k).args[0]) for k, v in ans.items()
        if 'other' not in k
        if v
    ]
    if "other_e" in ans and ans["other_e"]:
        items.append(
            ('other_e', ans['other']) if 'other' in ans else
            ('other_e', getattr(Tools, 'other_e').args[0])
        )
    return items


@survey_question('p5', 6)
def t1():
    """Q6/T1"""
    title = gettext('What are your preferred/more often used tools you use to run experiments? (check up to 3 tools)')
    def redir():
        t1_ans = t1_answers()
        if len(t1_ans) <= 1:
            erase(['t2', 't3'])
            return 'i1'
        if option('t2', '') not in {k for k, v in chain(t1_ans, [("no", 0)])}:
            erase(['t2', 't3'])
        return 't2'

    return form('t1', redir, title)


@survey_question('t1', 5)
def t2():
    """Q7/T2"""
    title = gettext('Which is your favorite tool for developing and running scientific experiments?')
    t1_ans = t1_answers()
    if len(t1_ans) <= 1:
        erase(['t2', 't3'])
        return goto('i1')

    options = t1_ans + Preference.options.kwargs['choices'][-1:]
    return form('t2', 't3', title, options=options)


@survey_question('t2', 5)
def t3():
    """Q8/T3"""
    title = gettext('What are the reasons for your preference? (check all that apply)')
    if answer('t2').get('options', {}) and option('t2', 'no') in {'no', 'None'}:
        erase('t3')
        return goto('i1')
    return form('t3', 'i1', title)


@survey_question('t1', 4)
def i1():
    """Q9/I1"""
    title = gettext('Have you ever used more than one tool in a single experiment?')
    return form('i1', 'i2', title)


@survey_question('i1', 4)
def i2():
    """Q10/I2"""
    title = gettext('Consider a collaborative science scenario where two teams execute variations of a given experiment and perform a joint analysis of these experiments, by comparing result data, methods, duration, and/or used parameters. In your experience, how likely is this scenario going to manifest itself in practice?')
    return form('i2', 'a1', title)


@survey_question('i2', 3)
def a1():
    """Q11/A1"""
    title = gettext('Have you ever analyzed provenance from your experiments?')
    return form('a1', 'a2', title)


@survey_question('a1', 3)
def a2():
    """Q12/A2"""
    title = gettext('What value if any do you seek from provenance analysis? (check all that apply)')
    if option('a1', '') in {'what_is_provenance',}:
        erase(['a2', 'a3', 'a4', 'a5'])
        return goto('c1')
    return form('a2', 'a3', title)


@survey_question('a2', 2)
def a3():
    """Q13/A3"""
    title = gettext('Which tools/languages have you ever used to analyze provenance? (check all that apply)')
    if option('a1', '') in {'what_is_provenance',}:
        erase(['a2', 'a3', 'a4', 'a5'])
        return goto(last(ORDER))
    if option('a1', '') in {'no', 'None'}:
        erase(['a3', 'a4', 'a5'])
        return goto('c1')
    return form('a3', 'a4', title)


@survey_question('a3', 2)
def a4():
    """Q14/A4"""
    title = gettext('Have you ever analyzed (or had to analyze) two or more provenance databases generated by variations of a given experiment together? This includes both the case of different teams running the experiments independently, as well as a single experimenter working on variants of an experiment.')
    return form('a4', 'a5', title)


@survey_question('a4', 2)
def a5():
    """Q15/A5"""
    title = gettext('These experiments were executed in different tools?')
    if option('a4') == 'no':
        erase('a5')
        return goto('c1')
    return form('a5', 'c1', title)


@survey_question('a1', 1)
def c1():
    """Q16/C1"""
    title = gettext('Would you accept being contacted about the possibility of participating in a practical experimental study about integrated provenance analysis? The study is in the context of a PhD thesis about provenance integration.')
    return form('c1', 'c2', title)


@survey_question('c1', 1)
def c2():
    """Q17/C2"""
    title = gettext('Would you accept being contacted to clarify some details about the answers you provided in this survey?')
    return form('c2', 'c3', title)


@survey_question('c2', 1)
def c3():
    """Q18/C3"""
    title = gettext('Please, enter your email so we can contact you.')
    if all(option(x) != 'yes' for x in ['c1', 'c2']):
        erase('c3')
        return goto('finish')
    return form('c3', 'finish', title)


@set_navbar(lazy_gettext('Thank you'))
def finish():
    """Thank you page"""
    save_answer('finish', {'submit': 'final'})
    lang = session['s_lang']
    session.clear()
    session['s_lang'] = lang
    session['s_minutes'] = gettext('Thank you')
    session['s_url'] = 'finish'
    return render_template('finish.html')
