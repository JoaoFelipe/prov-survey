# pylint: disable=line-too-long
"""Survey Forms"""
from flask_babel import lazy_gettext

from wtforms.fields import SubmitField, TextField, BooleanField, RadioField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email, DataRequired
from flask_wtf import FlaskForm



class StartForm(FlaskForm):
    """Index - Start"""
    submit = SubmitField(lazy_gettext('Start'))


class NextForm(FlaskForm):
    """Index - Restart"""
    submit = SubmitField(lazy_gettext('Restart'))
    next = SubmitField(lazy_gettext('Next'))

class Education(FlaskForm):
    """Q1/P1"""
    options = RadioField('', choices=[
        ('no', lazy_gettext('No schooling completed')),
        ('primary_progress', lazy_gettext('Primary School in progress')),
        ('primary', lazy_gettext('Primary School')),
        ('secondary_progress', lazy_gettext('Secondary Education in progress')),
        ('secondary', lazy_gettext('Secondary Education')),
        ('associate_progress', lazy_gettext('Associate degree in progress')),
        ('associate', lazy_gettext('Associate degree')),
        ('undergraduate_progress', lazy_gettext('Undergraduate degree in progress')),
        ('undergraduate', lazy_gettext('Undergraduate degree')),
        ('masters_progress', lazy_gettext(u'Masters degree in progress')),
        ('masters', lazy_gettext(u'Masters degree')),
        ('phd_progress', lazy_gettext('PhD degree in progress')),
        ('phd', lazy_gettext('PhD degree')),
    ])
    submit = SubmitField(lazy_gettext('Next'))


class ExperimentCount(FlaskForm):
    """Q2/P2"""
    options = RadioField('', choices=[
        ('0', lazy_gettext('0')),
        ('1', lazy_gettext('1')),
        ('2_to_5', lazy_gettext('2 to 5')),
        ('5_to_10', lazy_gettext('5 to 10')),
        ('more_than_10', lazy_gettext('More than 10')),
    ])
    submit = SubmitField(lazy_gettext('Next'))


class Experience(FlaskForm):
    """Q3/P3"""
    options = RadioField('', choices=[
        ('less_than_1', lazy_gettext('Less than 1 year')),
        ('1_to_2', lazy_gettext('Between 1 and 2 years')),
        ('2_to_5', lazy_gettext('Between 2 and 5 years')),
        ('5_to_7', lazy_gettext('Between 5 and 7 years')),
        ('7_to_12', lazy_gettext('Between 7 and 12 years')),
        ('more_than_12', lazy_gettext('More than 12 years')),
    ])
    submit = SubmitField(lazy_gettext('Next'))


class Situations(FlaskForm):
    """Q4/P4"""
    undergraduate_research = BooleanField(lazy_gettext('Undergraduate Research'))
    undergraduate_courses = BooleanField(lazy_gettext('Undergraduate Courses'))
    graduate_postgraduate_research = BooleanField(lazy_gettext('Graduate or Postgraduate Research'))
    university_research = BooleanField(lazy_gettext('Research (University)'))
    company_research = BooleanField(lazy_gettext('Research (Company)'))
    other_e = BooleanField(lazy_gettext('Other(s)'))
    other = TextField(lazy_gettext('Specify'))
    submit = SubmitField(lazy_gettext('Next'))


class Tools(FlaskForm):
    """Q5/U1"""
    wfms = BooleanField(lazy_gettext('Workflow Management Systems (eg.: VisTrails, Taverna, Kepler, SciCumulus, etc)'))
    script = BooleanField(lazy_gettext('Script Languages (eg.: Python, R, JavaScript, Julia, Matlab, etc)'))
    prog = BooleanField(lazy_gettext('System Programing languages (eg.: Java, C, C++, Fortran, Object Pascal, etc)'))
    submit = SubmitField(lazy_gettext('Next'))


class Workflows(FlaskForm):
    """Q6/U2"""
    askalon = BooleanField(lazy_gettext('Askalon'))
    esci_central = BooleanField(lazy_gettext('e-Science Central'))
    galaxy = BooleanField(lazy_gettext('Galaxy'))
    kepler = BooleanField(lazy_gettext('Kepler'))
    pegasus = BooleanField(lazy_gettext('Pegasus'))
    scicumulus = BooleanField(lazy_gettext('SciCumulus'))
    swift = BooleanField(lazy_gettext('Swift/T'))
    taverna = BooleanField(lazy_gettext('Taverna'))
    VisTrails = BooleanField(lazy_gettext('VisTrails'))
    other_e = BooleanField(lazy_gettext('Other(s)'))
    other = TextField(lazy_gettext('Specify'))
    submit = SubmitField(lazy_gettext('Next'))


class ScriptLanguages(FlaskForm):
    """Q7/U3"""
    idl = BooleanField(lazy_gettext('IDL'))
    javascript = BooleanField(lazy_gettext('Javascript'))
    julia = BooleanField(lazy_gettext('Julia'))
    matlab = BooleanField(lazy_gettext('Matlab'))
    perl = BooleanField(lazy_gettext('Perl'))
    python = BooleanField(lazy_gettext('Python'))
    r_lang = BooleanField(lazy_gettext('R'))
    s_lang = BooleanField(lazy_gettext('S'))
    shell = BooleanField(lazy_gettext('Shell script'))
    wolfram = BooleanField(lazy_gettext('Wolfram Language'))
    other_e = BooleanField(lazy_gettext('Other(s)2'))
    other = TextField(lazy_gettext('Specify'))
    submit = SubmitField(lazy_gettext('Next'))


class Preference(FlaskForm):
    """Q8/U4"""
    options = RadioField('', choices=[
        ('wfms', lazy_gettext('Workflow Management Systems')),
        ('script', lazy_gettext('Script Languages')),
        ('prog', lazy_gettext('System Programming Languages')),
        ('no', lazy_gettext('I do not have preferences')),
    ])
    submit = SubmitField(lazy_gettext('Next'))


class PreferenceReasons(FlaskForm):
    """Q9/U5"""
    setup = BooleanField(lazy_gettext('Easy to set up and run'))
    flexibility = BooleanField(lazy_gettext('Flexible development/modification'))
    provenance_capture = BooleanField(lazy_gettext('Provenance capture support'))
    provenance_analysis = BooleanField(lazy_gettext('Provenance analysis support'))
    experience = BooleanField(lazy_gettext('Previous experience (know-how)'))
    support = BooleanField(lazy_gettext('Helping/Supporting facilities'))
    learning = BooleanField(lazy_gettext('Easy to learn'))
    documentation = BooleanField(lazy_gettext('Documentation facilities'))
    share = BooleanField(lazy_gettext('Easy to share'))
    reproduce = BooleanField(lazy_gettext('Easy to reproduce'))
    other_e = BooleanField(lazy_gettext('Other(s)'))
    other = TextField(lazy_gettext('Specify'))
    submit = SubmitField(lazy_gettext('Next'))


class Analysis(FlaskForm):
    """Q10/A1"""
    options = RadioField('', choices=[
        ('yes', lazy_gettext('Yes')),
        ('no', lazy_gettext('No')),
        ('what_is_provenance', lazy_gettext('I do not know what is provenance'))
    ])
    submit = SubmitField(lazy_gettext('Next'))


class NoAnalysis(FlaskForm):
    """Q11/A2A"""
    deadline = BooleanField(lazy_gettext('Deadline'))
    no_utility = BooleanField(lazy_gettext('I do not see any utility'))
    no_tools = BooleanField(lazy_gettext('I do not have the appropriate tools'))
    no_knowledge = BooleanField(lazy_gettext('I do not have enough knowledge'))
    no_collection = BooleanField(lazy_gettext('I did not collect the provenance'))
    no_analysis = BooleanField(lazy_gettext('I did not reach the analysis phase'))
    other_e = BooleanField(lazy_gettext('Other(s)'))
    other = TextField(lazy_gettext('Specify'))
    submit = SubmitField(lazy_gettext('Next'))


class AnalysisTools(FlaskForm):
    """Q12/A2B"""
    SQL = BooleanField(lazy_gettext('SQL'))
    Prolog = BooleanField(lazy_gettext('Prolog'))
    Datalog = BooleanField(lazy_gettext('Datalog'))
    SPARQL = BooleanField(lazy_gettext('SPARQL'))
    XQuery = BooleanField(lazy_gettext('XQuery'))
    XPath = BooleanField(lazy_gettext('XPath'))
    wfms = BooleanField(lazy_gettext('Workflow Management Systems'))
    script_e = BooleanField(lazy_gettext('Script Languages'))
    script = TextField(lazy_gettext('Specify'))
    prog_e = BooleanField(lazy_gettext('System Programming Languages'))
    prog = TextField(lazy_gettext('Specify'))
    other_e = BooleanField(lazy_gettext('Other(s)2'))
    other = TextField(lazy_gettext('Specify'))
    submit = SubmitField(lazy_gettext('Next'))


class Integration(FlaskForm):
    """Q13/I1"""
    options = RadioField('', choices=[
        ('distinct_wfms ', lazy_gettext('Yes, I have used distinct Workflow Management Systems')),
        ('distinct_script', lazy_gettext('Yes, I have used distinct Script Languages')),
        ('distinct_prog', lazy_gettext('Yes, I have used distinct System Programming Languages')),
        ('wfms,script', lazy_gettext('Yes, I have used Workflow Management Systems and Script Languages')),
        ('wfms,prog', lazy_gettext('Yes, I have used Workflow Management Systems and System Programming Languages')),
        ('script,prog', lazy_gettext('Yes, I have used Script Languages and System Programming Languages')),
        ('wfms,script,prog', lazy_gettext('Yes, I have used all types of tools')),
        ('no', lazy_gettext('No, I have never combined multiple tools'))
    ])
    submit = SubmitField(lazy_gettext('Next'))


class YesNo(FlaskForm):
    """Q14/I2, Q15/I3, Q16/I4, Q17/F1, Q18/F2"""
    options = RadioField('', choices=[
        ('yes', lazy_gettext('Yes')),
        ('no', lazy_gettext('No')),
    ])
    submit = SubmitField(lazy_gettext('Next'))


class EmailForm(FlaskForm):
    """Q19/F3"""
    email = TextField('', [
        DataRequired(lazy_gettext('You must specify the email!')),
        Email(lazy_gettext('The email must be valid!')),
    ])
    submit = SubmitField(lazy_gettext('Finish'))
