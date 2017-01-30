"""Survey questions"""
# pylint: disable=invalid-name
# pylint: disable=line-too-long

import os
import binascii
from collections import OrderedDict

from flask import session, render_template
from flask_babel import gettext, lazy_gettext

from .db import db, Answer

from .helper import erase, goto, question_form, radio_question, last, answer
from .helper import option, set_navbar, survey_question, save_answer

from .forms import StartForm, NextForm
from .forms import Education, ExperimentCount, Experience, Situations
from .forms import Tools, Workflows, ScriptLanguages
from .forms import Preference, PreferenceReasons
from .forms import Analysis, NoAnalysis, AnalysisTools, Integration
from .forms import EmailForm, YesNo

FORMS = OrderedDict([
    ('p1', Education),
    ('p2', ExperimentCount),
    ('p3', Experience),
    ('p4', Situations),
    ('t', Tools),
    ('w', Workflows),
    ('s', ScriptLanguages),
    ('c', Preference),
    ('r', PreferenceReasons),
    ('a1', Analysis),
    ('a2a', NoAnalysis),
    ('a2b', AnalysisTools),
    ('i1', Integration),
    ('i2', YesNo),
    ('i3', YesNo),
    ('i4', YesNo),
    ('f1', YesNo),
    ('f2', YesNo),
    ('f3', EmailForm),
])

ORDER = [x.upper() for x in FORMS.keys()] + ['finish']


def form(number, next_question, title):
    """Question Form based on Form type"""
    form_class = FORMS[number]
    question_function = (
        question_form if form_class._mode != 'radio' else radio_question
    )
    return question_function(number, next_question, form_class, title)


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


@survey_question('p2', 8)
def p3():
    """Q3/P3"""
    title = gettext('How much experience do you have in running scientific experiments on computational environments?')
    return form('p3', 'p4', title)


@survey_question('p3', 7)
def p4():
    """Q4/P4"""
    title = gettext('In which situations have you performed computational experiments? (check all that apply)')
    return form('p4', 't', title)


@survey_question('p4', 7)
def t():
    """Q5/T"""
    title = gettext('Which computational tools have you ever used to run your experiments? (check all that apply)')
    def redir():
        """Select next acoording to choosen option"""
        ans = answer('t')
        quantity = sum(1 for x in ans.values() if x)
        erase_list = []
        if not ans.get('wfms', False):
            erase_list.append('w')
        if not ans.get('script', False):
            erase_list.append('s')
        if quantity == 1:
            erase_list.append('c')
        erase(erase_list)
        if quantity == 0:
            erase(['w', 's', 'c', 'r'])
            return 'finish'
        return 'w'
    return form('t', redir, title)


@survey_question('t', 6)
def w():
    """Q6/W"""
    title = gettext('Which Workflow Management Systems have you ever used to run scientific experiments (check all that apply)')
    if sum(1 for x in answer('t').values() if x) == 0:
        erase('w')
        return goto('t')
    if not answer('t').get('wfms', False):
        erase('w')
        return goto('s')
    return form('w', 's', title)


@survey_question([('t', 'w')], 6)
def s():
    """Q7/S"""
    title = gettext('Which Script Languages have you ever used to run scientific experiments (check all that apply)')
    if sum(1 for x in answer('t').values() if x) == 0:
        erase('s')
        return goto('t')
    if not answer('t').get('script', False):
        erase('s')
        return goto('c')
    return form('s', 'c', title)


@survey_question([('t', 'w', 's')], 5)
def c():
    """Q8/C"""
    title = gettext('Which is your favorite tool for developing and running scientific experiments?')
    if sum(1 for x in answer('t').values() if x) == 0:
        erase('c')
        return goto('t')
    if sum(1 for x in answer('t').values() if x) < 2:
        erase('c')
        return goto('r')
    return form('c', 'r', title)


@survey_question([('t', 'w', 's', 'c')], 5)
def r():
    """Q9/R"""
    title = gettext('What are the reasons for your preference? (check all that apply)')
    quantity = sum(1 for x in answer('t').values() if x)
    if quantity == 0:
        erase('r')
        return goto('t')
    if quantity > 1:
        if answer('c').get('options', {}) and option('c', 'no') in {'no', 'None'}:
            erase('r')
            return goto('a1')
    return form('r', 'a1', title)


@survey_question([('w', 's', 'c', 'r')], 4)
def a1():
    """Q10/A1"""
    title = gettext('Have you ever analyzed provenance generated from the execution of scientific experiments?')
    def redir():
        """Select next acoording to choosen option"""
        opt = option('a1', 'yes')
        if opt in {'yes', 'None'}:
            erase('a2a')
            return 'a2b'
        if opt == 'no':
            erase('a2b')
            return 'a2a'
        if opt == 'what_is_provenance':
            return 'finish'
    return form('a1', redir, title)


@survey_question('a1', 4)
def a2a():
    """Q11/A2A"""
    title = gettext('Why did you not analyze provenance data? (check all that apply)')
    if option('a1', 'yes') in {'yes', 'None'}:
        erase('a2a')
        return goto(last(ORDER))
    return form('a2a', 'i1', title)


@survey_question('a1', 4)
def a2b():
    """Q12/A2B"""
    title = gettext('Which tools/languages have you ever used to analyze provenance? (check all that apply)')
    if option('a1', 'yes') == 'no':
        erase('a2b')
        return goto(last(ORDER))
    return form('a2b', 'i1', title)


@survey_question([('a2a', 'a2b')], 3)
def i1():
    """Q13/I1"""
    title = gettext('Have you ever used more than one tool in a single experiment?')
    return form('i1', 'i2', title)


@survey_question('i1', 2)
def i2():
    """Q14/I2"""
    title = gettext('In your understanding, when two team execute variations of a given experiment, is there any advantage in performing a joint analysis of these experiments, by comparing result data, methods, duration, and/or used parameters?')
    return form('i2', 'i3', title)


@survey_question('i2', 2)
def i3():
    """Q15/I3"""
    title = gettext('Have you ever analyzed (or had to analyze) two or more provenance databases generated by variations of a given experiment together? Note that different teams with different machines might have executed these experiments, or a single person might have executed the variations.')
    return form('i3', 'i4', title)


@survey_question('i3', 2)
def i4():
    """Q16/I4"""
    title = gettext('These experiments were executed in different tools?')
    if option('i3') == 'no':
        erase('i4')
        return goto('f1')
    return form('i4', 'f1', title)


@survey_question([('i3', 'i4')], 1)
def f1():
    """Q17/F1"""
    title = gettext('Would you accept being contacted about the possibility of participating in a practical experimental study about integrated provenance analysis? The study is in the context of a PhD thesis about provenance integration.')
    return form('f1', 'f2', title)


@survey_question('f1', 1)
def f2():
    """Q18/F2"""
    title = gettext('Would you accept being contacted to clarify some details about the answers you provided in this survey?')
    return form('f2', 'f3', title)


@survey_question('f2', 1)
def f3():
    """Q19/F3"""
    title = gettext('Please, enter your email so we can contact you.')
    if all(option(x) != 'yes' for x in ['f1', 'f2']):
        erase('f3')
        return goto('finish')
    return form('f3', 'finish', title)


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
