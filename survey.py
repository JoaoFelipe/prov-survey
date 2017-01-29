"""Survey questions"""
# pylint: disable=invalid-name
# pylint: disable=line-too-long

import os
import binascii

from flask import session, render_template
from flask_babel import gettext, lazy_gettext


from .helper import erase, goto, question_form, radio_question, last, answer
from .helper import option, set_navbar, survey_question

from .forms import StartForm, NextForm
from .forms import Education, ExperimentCount, Experience, Situations
from .forms import Tools, Workflows, ScriptLanguages
from .forms import Preference, PreferenceReasons
from .forms import Analysis, NoAnalysis, AnalysisTools, Integration
from .forms import EmailForm, YesNo


ORDER = [
    'P1', 'P2', 'P3', 'P4',
    'U1', 'U2', 'U3', 'U4', 'U5',
    'A1', 'A2A', 'A2B',
    'I1', 'I2', 'I3',
    'I4', 'F1', 'F2', 'F3',
    'finish'
]


@set_navbar(9)
def index():
    """First page"""
    lang = session['s_lang']
    form = (NextForm if 's_uid' in session else StartForm)()
    if form.validate_on_submit():
        if form.submit.data:
            session.clear()
            session['s_lang'] = lang
            session['s_index'] = True
            session['s_uid'] = binascii.hexlify(os.urandom(24))
            # ToDo: save
        session['s_p1'] = True
        return goto('p1')
    return render_template('index.html', form=form)


@survey_question("index", 8)
def p1():
    """Q1/P1"""
    title = gettext("What is your educational level?")
    return radio_question('p1', 'p2', Education, title)


@survey_question("p1", 8)
def p2():
    """Q2/P2"""
    title = gettext("How many scientific experiments have you ever performed on computational environments?")
    return radio_question('p2', (lambda: 'p3' if option('p2') != '0' else 'finish'), ExperimentCount, title)


@survey_question("p2", 8)
def p3():
    """Q3/P3"""
    title = gettext("How much experience do you have in running scientific experiments on computational environments?")
    return radio_question('p3', 'p4', Experience, title)


@survey_question("p3", 7)
def p4():
    """Q4/P4"""
    title = gettext("In which situations have you performed computational experiments? (check all that apply)")
    return question_form('p4', 'u1', Situations, title)


@survey_question("p4", 7)
def u1():
    """Q5/U1"""
    title = gettext("Which computational tools have you ever used to run your experiments? (check all that apply)")
    def redir():
        """Select next acoording to choosen option"""
        if sum(1 for x in answer('u1').values() if x) == 0:
            return 'finish'
        return 'u2'
    return question_form('u1', redir, Tools, title)


@survey_question("u1", 6)
def u2():
    """Q6/U2"""
    title = gettext("Which Workflow Management Systems have you ever used to run scientific experiments (check all that apply)")
    if sum(1 for x in answer('u1').values() if x) == 0:
        erase('u2')
        return goto('u1')
    if not answer('u1').get('wfms', False):
        erase('u2')
        return goto('u3')
    return question_form('u2', 'u3', Workflows, title)


@survey_question([("u1", "u2")], 6)
def u3():
    """Q7/U3"""
    title = gettext("Which Script Languages have you ever used to run scientific experiments (check all that apply)")
    if sum(1 for x in answer('u1').values() if x) == 0:
        erase('u3')
        return goto('u1')
    if not answer('u1').get('script', False):
        erase('u3')
        return goto('u4')
    return question_form('u3', 'u4', ScriptLanguages, title)


@survey_question([("u1", "u2", "u3")], 5)
def u4():
    """Q8/U4"""
    title = gettext("Which is your favorite tool for developing and running scientific experiments?")
    if sum(1 for x in answer('u1').values() if x) == 0:
        erase('u4')
        return goto('u1')
    if sum(1 for x in answer('u1').values() if x) < 2:
        erase('u4')
        return goto('u5')
    return radio_question('u4', 'u5', Preference, title)


@survey_question([("u1", "u2", "u3", "u4")], 5)
def u5():
    """Q9/U5"""
    title = gettext("What are the reasons for your preference? (check all that apply)")
    if sum(1 for x in answer('u1').values() if x) == 0:
        erase('u5')
        return goto('u1')
    if sum(1 for x in answer('u1').values() if x) > 1:
        if answer('u4').get('options', {}) and option('u4', 'no') in {'no', 'None'}:
            erase('u5')
            return goto('a1')
    return question_form('u5', 'a1', PreferenceReasons, title)


@survey_question([("u2", "u3", "u4", "u5")], 4)
def a1():
    """Q10/A1"""
    title = gettext("Have you ever analyzed provenance generated from the execution of scientific experiments?")
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
    return radio_question('a1', redir, Analysis, title)


@survey_question("a1", 4)
def a2a():
    """Q11/A2A"""
    title = gettext("Why did you not analyze provenance data? (check all that apply)")
    if option('a1', 'yes') in {'yes', 'None'}:
        erase('a2a')
        return goto(last(ORDER))
    return question_form('a2a', 'i1', NoAnalysis, title)


@survey_question("a1", 4)
def a2b():
    """Q12/A2B"""
    title = gettext("Which tools/languages have you ever used to analyze provenance? (check all that apply)")
    if option('a1', 'yes') == 'no':
        erase('a2b')
        return goto(last(ORDER))
    return question_form('a2b', 'i1', AnalysisTools, title)


@survey_question([("a2a", "a2b")], 3)
def i1():
    """Q13/I1"""
    title = gettext("Have you ever used more than one tool in a single experiment?")
    return radio_question('i1', 'i2', Integration, title)


@survey_question("i1", 2)
def i2():
    """Q14/I2"""
    title = gettext("In your understanding, when two team execute variations of a given experiment, is there any advantage in performing a joint analysis of these experiments, by comparing result data, methods, duration, and/or used parameters?")
    return radio_question('i2', 'i3', YesNo, title)


@survey_question("i2", 2)
def i3():
    """Q15/I3"""
    title = gettext("Have you ever analyzed (or had to analyze) two or more provenance databases generated by variations of a given experiment together? Note that different teams with different machines might have executed these experiments, or a single person might have executed the variations.")
    return radio_question('i3', 'i4', YesNo, title)


@survey_question("i3", 2)
def i4():
    """Q16/I4"""
    title = gettext("These experiments were executed in different tools?")
    if option('i3') == 'no':
        erase('i4')
        return goto('f1')
    return radio_question('i4', 'f1', YesNo, title)


@survey_question([("i3", "i4")], 1)
def f1():
    """Q17/F1"""
    title = gettext("Would you accept being contacted about the possibility of participating in a practical experimental study about integrated provenance analysis? The study is in the context of a PhD thesis about provenance integration.")
    return radio_question('f1', 'f2', YesNo, title)


@survey_question("f1", 1)
def f2():
    """Q18/F2"""
    title = gettext("Would you accept being contacted to clarify some details about the answers you provided in this survey?")
    return radio_question('f2', 'f3', YesNo, title)


@survey_question("f2", 1)
def f3():
    """Q19/F3"""
    title = gettext('Please, enter your email so we can contact you.')
    if all(option(x) != 'yes' for x in ['f1', 'f2']):
        erase('f3')
        return goto('finish')
    return question_form('f3', 'finish', EmailForm, title)


@set_navbar(lazy_gettext("Thank you"))
def finish():
    """Thank you page"""
    lang = session['s_lang']
    session.clear()
    session['s_lang'] = lang
    session["s_minutes"] = gettext("Thank you")
    session['s_url'] = 'finish'
    return render_template('finish.html')
