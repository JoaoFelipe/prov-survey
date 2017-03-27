# pylint: disable=line-too-long
"""Survey Forms"""
from collections import OrderedDict

from flask_babel import lazy_gettext, gettext

from wtforms.fields import SubmitField, TextField, BooleanField
from wtforms.fields import RadioField, SelectField
from wtforms.fields.core import UnboundField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email, DataRequired
from flask_wtf import FlaskForm

import pycountry

class Form(FlaskForm):
    """Survey Form BaseClass"""

    @classmethod
    def survey_fields(cls):
        """Return form fields"""
        return [attr for attr, value in cls.__dict__.items()
                if isinstance(value, UnboundField)
                if value.field_class is not SubmitField]

    @classmethod
    def survey_unbound_fields(cls):
        """Return form fields"""
        return [attr
                for attr, value in cls._unbound_fields or cls.__dict__.items()
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
        if answer.get(field, '') in ('', 'None') or unbound.field_class is not RadioField:
            return None
        extra = ''
        raw_name = str(answer[field])
        if raw_name.endswith('_e') and raw_name[:-2] in answer:
            extra = '({})'.format(answer[raw_name[:-2]])
        if raw:
            return raw_name + extra
        try:
            name = str(dict(unbound.kwargs['choices'])[raw_name])
            return name + extra
        except KeyError:
            if not hasattr(cls, '_dynamic_checkform'):
                raise
            return cls._dynamic_checkform.survey_field_answer(
                raw_name, {raw_name: 'True'}, raw=raw
            )



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


class Domains(CheckForm):
    """Q3/P3"""
    biology = BooleanField(lazy_gettext('Biological Sciences'))
    computer = BooleanField(lazy_gettext('Computer and Information Sciences'))
    education = BooleanField(lazy_gettext('Education'))
    engineering = BooleanField(lazy_gettext('Engineering'))
    geosciences = BooleanField(lazy_gettext('Geosciences'))
    math = BooleanField(lazy_gettext('Mathematical Sciences'))
    social = BooleanField(lazy_gettext('Social, Behavioral and Economic Sciences'))
    other_e = BooleanField(lazy_gettext('Other(s)'))
    other = TextField(lazy_gettext('Specify'))
    submit = SubmitField(lazy_gettext('Next'))


class Experience(RadioForm):
    """Q4/P4"""
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
    """Q5/P5"""
    undergraduate_research = BooleanField(lazy_gettext('Undergraduate Student in a Undergraduate Research'))
    undergraduate_courses = BooleanField(lazy_gettext('Undergraduate Student in a Course'))
    masters = BooleanField(lazy_gettext('Masters Student'))
    phd = BooleanField(lazy_gettext('Ph.D. Student/Candidate'))
    postdoc = BooleanField(lazy_gettext('Postdoctoral Researcher'))
    university = BooleanField(lazy_gettext('University Researcher'))
    company = BooleanField(lazy_gettext('Company Researcher'))
    principal = BooleanField(lazy_gettext('Principal Investigator'))
    other_e = BooleanField(lazy_gettext('Other(s)'))
    other = TextField(lazy_gettext('Specify'))
    submit = SubmitField(lazy_gettext('Next'))


class CountrySelectField(SelectField):
    def __init__(self, *args, **kwargs):
        super(CountrySelectField, self).__init__(*args, **kwargs)
        self.choices = (
            [("", "")] +
            sorted(
                [(country.alpha_3, "{}".format(country.name))
                 for country in pycountry.countries],
                key=lambda e: e[1]
            )

        )

class Country(TextForm):
    """Q/P6"""
    country = CountrySelectField('')
    submit = SubmitField(lazy_gettext('Next'))



class Tools(CheckForm):
    """Q6/T1"""
    limit = 3
    _categories = lambda c: OrderedDict([
        (lazy_gettext("Workflow Management Systems"), [
            "askalon", "chiron", "esci_central", "galaxy", "kepler", "pegasus",
            "scicumulus", "swift", "taverna", "vistrails",
        ]),
        (lazy_gettext("Script Languages"), [
            "idl", "javascript", "julia", "matlab", "perl", "python",
            "r_lang", "s_lang", "shell", "wolfram"
        ]),
        (lazy_gettext("System Programming Languages"), [
            "c", "cpp", "fortran", "java", "object_pascal",
        ]),
        ("__other__", [
            "other_e", "other", "submit"
        ])
    ])

    askalon = BooleanField(lazy_gettext('Askalon'))
    chiron = BooleanField(lazy_gettext('Chiron'))
    esci_central = BooleanField(lazy_gettext('e-Science Central'))
    galaxy = BooleanField(lazy_gettext('Galaxy'))
    kepler = BooleanField(lazy_gettext('Kepler'))
    pegasus = BooleanField(lazy_gettext('Pegasus'))
    scicumulus = BooleanField(lazy_gettext('SciCumulus'))
    swift = BooleanField(lazy_gettext('Swift/T'))
    taverna = BooleanField(lazy_gettext('Taverna'))
    vistrails = BooleanField(lazy_gettext('VisTrails'))

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

    c = BooleanField(lazy_gettext('C'))
    cpp = BooleanField(lazy_gettext('C++'))
    fortran = BooleanField(lazy_gettext('Fortran'))
    java = BooleanField(lazy_gettext('Java'))
    object_pascal = BooleanField(lazy_gettext('Object Pascal'))

    other_e = BooleanField(lazy_gettext('Other(s)2'))
    other = TextField(lazy_gettext('Specify'))
    submit = SubmitField(lazy_gettext('Next'))



class Preference(RadioForm):
    """Q7/T2"""
    _dynamic_checkform = Tools
    options = RadioField('', choices=[
        ('no', lazy_gettext('I do not have preferences')),
    ])
    submit = SubmitField(lazy_gettext('Next'))


class PreferenceReasons(CheckForm):
    """Q8/T3"""
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


class Integration(RadioForm):
    """Q9/I1"""
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


class Likelyhood(RadioForm):
    """Q10/I2"""
    options = RadioField('', choices=[
        ('1', lazy_gettext('Not at all likely')),
        ('2', lazy_gettext('Slightly likely')),
        ('3', lazy_gettext('Moderately likely')),
        ('4', lazy_gettext('Very likely')),
        ('5', lazy_gettext('Completely likely')),
    ])
    submit = SubmitField(lazy_gettext('Next'))


class Analysis(RadioForm):
    """Q10/A1"""
    options = RadioField('', choices=[
        ('yes', lazy_gettext('Yes')),
        ('no', lazy_gettext('No')),
        ('what_is_provenance', lazy_gettext('I do not know what is provenance'))
    ])
    submit = SubmitField(lazy_gettext('Next'))


class AnalysisReasons(CheckForm):
    """Q12/A2"""
    comprehensive_2 = BooleanField(lazy_gettext('I value it for comprehending the experiment'))
    reproducibility_2 = BooleanField(lazy_gettext('I value it for reproducing the experiment'))
    no_time_1 = BooleanField(lazy_gettext('I value it, but I do not have time for analyses'))
    no_tools_1 = BooleanField(lazy_gettext('I value it, but I do not have the appropriate tools'))
    no_knowledge_1 = BooleanField(lazy_gettext('I value it, but I do not have enough knowledge'))
    no_utility_0 = BooleanField(lazy_gettext('I do not see any utility in provenance analysis'))
    other_e = BooleanField(lazy_gettext('Other(s)'))
    other = TextField(lazy_gettext('Specify'))
    submit = SubmitField(lazy_gettext('Next'))


class AnalysisTools(CheckForm):
    """Q13/A3"""
    SQL = BooleanField(lazy_gettext('SQL'))
    Prolog = BooleanField(lazy_gettext('Prolog'))
    Datalog = BooleanField(lazy_gettext('Datalog'))
    SPARQL = BooleanField(lazy_gettext('SPARQL'))
    XQuery = BooleanField(lazy_gettext('XQuery'))
    XPath = BooleanField(lazy_gettext('XPath'))
    wfms_e = BooleanField(lazy_gettext('Workflow Management Systems'))
    wfms = TextField(lazy_gettext('Specify'))
    script_e = BooleanField(lazy_gettext('Script Languages'))
    script = TextField(lazy_gettext('Specify'))
    prog_e = BooleanField(lazy_gettext('System Programming Languages'))
    prog = TextField(lazy_gettext('Specify'))
    other_e = BooleanField(lazy_gettext('Other(s)2'))
    other = TextField(lazy_gettext('Specify'))
    submit = SubmitField(lazy_gettext('Next'))



class YesNo(RadioForm):
    """Q11/I3, Q14/A4, Q15/A5, Q16/C1, Q17/C2"""
    options = RadioField('', choices=[
        ('yes', lazy_gettext('Yes')),
        ('no', lazy_gettext('No')),
    ])
    submit = SubmitField(lazy_gettext('Next'))


class EmailForm(TextForm):
    """Q18/F3"""
    email = TextField('', [
        DataRequired(lazy_gettext('You must specify the email!')),
        Email(lazy_gettext('The email must be valid!')),
    ])
    submit = SubmitField(lazy_gettext('Next'))

class Institution(TextForm):
    """Q/P7"""
    institution = TextField(lazy_gettext('Institution'))
    role = TextField(lazy_gettext('Role'))
    submit = SubmitField(lazy_gettext('Finish'))
