# pylint: disable=line-too-long
"""Survey Forms"""
from collections import OrderedDict

from flask_babel import lazy_gettext

from wtforms.fields import SubmitField, TextField, BooleanField
from wtforms.fields import RadioField
from wtforms.fields.core import UnboundField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email, DataRequired
from flask_wtf import FlaskForm



class Form(FlaskForm):
    """Survey Form BaseClass"""

    @classmethod
    def survey_fields(cls):
        """Return form fields"""
        return [attr for attr, value in cls.__dict__.items()
                if isinstance(value, UnboundField)
                if value.field_class is not SubmitField]

    @classmethod
    def survey_field_answer(cls, field, answer, raw=False):  # pylint: disable=unused-argument
        """Return field answer as str"""
        if field not in answer:
            return None
        return str(answer[field])


    @classmethod
    def survey_answers(cls, answer, raw=False, sep=', '):
        """Return field answers for a user"""
        if answer is None:
            return ''
        result = []
        for field in cls.survey_fields():
            ans = cls.survey_field_answer(field, answer, raw=raw)
            if ans is not None:
                result.append(ans)
        return sep.join(result)


class RadioForm(Form):
    """Survey RadioForm BaseClass"""
    _mode = 'radio'

    @classmethod
    def survey_field_answer(cls, field, answer, raw=False):
        unbound = getattr(cls, field)
        if field not in answer or unbound.field_class is not RadioField:
            return None
        extra = ''
        raw_name = str(answer[field])
        if raw_name.endswith('_e') and raw_name[:-2] in answer:
            extra = '({})'.format(answer[raw_name[:-2]])
        if raw:
            return raw_name + extra
        name = str(dict(unbound.kwargs['choices'])[raw_name])
        return name + extra



class CheckForm(Form):
    """Survey CheckForm BaseClass"""
    _mode = 'check'

    @classmethod
    def survey_field_answer(cls, field, answer, raw=False):
        unbound = getattr(cls, field)
        is_not_boolean = unbound.field_class is not BooleanField
        if answer.get(field, '') != 'True' or is_not_boolean:
            return None
        extra = ''
        if field.endswith('_e') and field[:-2] in answer:
            extra = '({})'.format(answer[field[:-2]])
        if raw:
            return field + extra
        name = str(unbound.args[0])
        return name + extra


class TextForm(Form):
    """Survey TextForm BaseClass"""
    _mode = 'text'


class StartForm(Form):
    """Index - Start"""
    submit = SubmitField(lazy_gettext('Start'))


class NextForm(Form):
    """Index - Restart"""
    submit = SubmitField(lazy_gettext('Restart'))
    next = SubmitField(lazy_gettext('Next'))

class Education(RadioForm):
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


class ExperimentCount(RadioForm):
    """Q2/P2"""
    options = RadioField('', choices=[
        ('0', lazy_gettext('0')),
        ('1', lazy_gettext('1')),
        ('2_to_5', lazy_gettext('2 to 5')),
        ('5_to_10', lazy_gettext('5 to 10')),
        ('more_than_10', lazy_gettext('More than 10')),
    ])
    submit = SubmitField(lazy_gettext('Next'))


class Experience(RadioForm):
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


class Situations(CheckForm):
    """Q4/P4"""
    undergraduate_research = BooleanField(lazy_gettext('Undergraduate Research'))
    undergraduate_courses = BooleanField(lazy_gettext('Undergraduate Courses'))
    graduate_postgraduate_research = BooleanField(lazy_gettext('Graduate or Postgraduate Research'))
    university_research = BooleanField(lazy_gettext('Research (University)'))
    company_research = BooleanField(lazy_gettext('Research (Company)'))
    other_e = BooleanField(lazy_gettext('Other(s)'))
    other = TextField(lazy_gettext('Specify'))
    submit = SubmitField(lazy_gettext('Next'))


class Tools(CheckForm):
    """Q5/T"""
    wfms = BooleanField(lazy_gettext('Workflow Management Systems (eg.: VisTrails, Taverna, Kepler, SciCumulus, etc)'))
    script = BooleanField(lazy_gettext('Script Languages (eg.: Python, R, JavaScript, Julia, Matlab, etc)'))
    prog = BooleanField(lazy_gettext('System Programing languages (eg.: Java, C, C++, Fortran, Object Pascal, etc)'))
    submit = SubmitField(lazy_gettext('Next'))


class Workflows(CheckForm):
    """Q6/W"""
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


class ScriptLanguages(CheckForm):
    """Q7/S"""
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


class Preference(RadioForm):
    """Q8/C"""
    options = RadioField('', choices=[
        ('wfms', lazy_gettext('Workflow Management Systems')),
        ('script', lazy_gettext('Script Languages')),
        ('prog', lazy_gettext('System Programming Languages')),
        ('no', lazy_gettext('I do not have preferences')),
    ])
    submit = SubmitField(lazy_gettext('Next'))


class PreferenceReasons(CheckForm):
    """Q9/R"""
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


class Analysis(RadioForm):
    """Q10/A1"""
    options = RadioField('', choices=[
        ('yes', lazy_gettext('Yes')),
        ('no', lazy_gettext('No')),
        ('what_is_provenance', lazy_gettext('I do not know what is provenance'))
    ])
    submit = SubmitField(lazy_gettext('Next'))


class NoAnalysis(CheckForm):
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


class AnalysisTools(CheckForm):
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


class Integration(RadioForm):
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


class YesNo(RadioForm):
    """Q14/I2, Q15/I3, Q16/I4, Q17/F1, Q18/F2"""
    options = RadioField('', choices=[
        ('yes', lazy_gettext('Yes')),
        ('no', lazy_gettext('No')),
    ])
    submit = SubmitField(lazy_gettext('Next'))


class EmailForm(TextForm):
    """Q19/F3"""
    email = TextField('', [
        DataRequired(lazy_gettext('You must specify the email!')),
        Email(lazy_gettext('The email must be valid!')),
    ])
    submit = SubmitField(lazy_gettext('Finish'))
