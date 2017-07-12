"""Navbar and routes"""
import subprocess
import traceback
from io import StringIO
from os.path import join, expanduser
from itertools import groupby

from flask import Blueprint, session, request, current_app, jsonify
from flask_babel import lazy_gettext
from flask_mail import Message

from sqlalchemy import select

from . import survey
from .babel import babel
from .db import db, Answer
from .helper import local_view, last, goto, answer, create_csv
from .mail import mail
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
                    view.classes = ['unanswered']
                elif len(ans) == sum(1 for x in ans.values() if not x):
                    view.classes = ['unanswered']
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

@frontend.route('/scipy')
def scipy():
    """Redirect to en"""
    session['s_origin'] = 'scipy'
    session['s_lang'] = 'en'
    return goto('index')

@frontend.route('/clear')
def clear():
    """Redirect to en"""
    session.clear()
    return goto('index')



@frontend.route('/send/<lang>/<receiver>/')
def send(lang, receiver):
    """send results"""
    raw = False
    languages = current_app.config['LANGUAGES']
    if lang == 'raw' or lang not in languages:
        raw = True
    else:
        session['s_lang'] = lang

    csvfile = StringIO()
    create_csv(csvfile, survey.FORMS, sep=',', internal_sep=';', raw=raw)
    csvfile.seek(0)

    if receiver == "github":
        try:
            import nbformat
            from nbconvert.preprocessors import ExecutePreprocessor

            output = []
            github_path = expanduser(current_app.config["GITHUB"])
            csv_path = join(github_path, "..", "survey_result.csv")
            with open(csv_path, "w") as csv:
                csv.write(csvfile.read())
            output.append("Wrote survey_result.csv")

            output.append("Pulling GitHub repository")
            pull = subprocess.check_output(["git", "pull"], cwd=github_path)
            output.append(pull.decode("utf-8"))
            output.append("Converting notebook to html")
            survey_analysis_path = join(github_path, "survey_analysis")
            with open(join(survey_analysis_path, "Analysis.ipynb")) as f:
                nb = nbformat.read(f, 4)
            ep = ExecutePreprocessor()
            ep.preprocess(nb, {'metadata': {'path': survey_analysis_path}})
            with open(join(survey_analysis_path, 'Automatic.ipynb'), 'wt') as f:
                nbformat.write(nb, f)

            '''
            nbconvert = subprocess.check_output([
                "jupyter", "nbconvert",
                "--to", "notebook",
                "--output", "Automatic.ipynb",
                "--execute",
                "Analysis.ipynb"
            ], cwd=survey_analysis_path)

            output.append(nbconvert.decode("utf-8"))
            '''
            output.append("Commiting changes")
            commit = subprocess.check_output([
                "git", "commit", "-am", "Automatic generation"], cwd=github_path)
            output.append(commit.decode("utf-8"))
            output.append("Pushing GitHub repository")
            pull = subprocess.check_output(["git", "push"], cwd=github_path)

            return "<br>".join(output)
        except:
            return traceback.format_exc().replace("\n", "<br>")

    if current_app.config['MAIL_USERNAME'] is None:
        return '<br>'.join(csvfile.readlines())

    if receiver not in current_app.config['CONTACTS']:
        return 'Invalid receiver'

    recipient = '@'.join(current_app.config['CONTACTS'][receiver])
    msg = Message('Survey Results',
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[recipient])
    msg.body = 'Find the survey results attached'
    msg.attach('result.csv', 'text/csv', csvfile.read())
    mail.send(msg)
    return 'Email sent to {}'.format(recipient)


@frontend.route('/<lang>/', defaults={'number': 'index'}, methods=GET_POST)
@frontend.route('/<lang>/<number>/', methods=GET_POST)
def question(lang, number):
    """Survey question routes"""
    languages = current_app.config['LANGUAGES']
    session['s_lang'] = lang if lang in languages else 'en'
    if hasattr(survey, number):
        return getattr(survey, number)()
    return goto(last(survey.ORDER))


@frontend.route('/translation/<lang>/')
def translation(lang):
    """Create json with translations"""
    from collections import OrderedDict
    languages = current_app.config['LANGUAGES']
    session['s_lang'] = lang if lang in languages else 'en'

    result = OrderedDict()
    result["_order"] = []
    for qnum, form in survey.FORMS.items():
        result["_order"].append(qnum)
        tit = ''
        result[qnum] = {}
        result[qnum]['title'] = survey.TITLES[qnum]
        result[qnum]['answers'] = OrderedDict()
        result[qnum]['answer_order'] = []
        fields_e = []
        for field in form.survey_unbound_fields():
            field_obj = getattr(form, field)
            if field == 'options':
                for raw, ans in field_obj.kwargs['choices']:
                    result[qnum]['answer_order'].append(raw)
                    result[qnum]['answers'][raw] = str(ans)
            else:
                if field.endswith('_e'):
                    fields_e.append(field)
                else:
                    result[qnum]['answer_order'].append(field)
                result[qnum]['answers'][field] = str(field_obj.args[0])

        for field_e in fields_e:
            field = field_e[:-2]
            result[qnum]['answers'][field] = result[qnum]['answers'][field_e]
            del result[qnum]['answers'][field_e]

    return jsonify(result)
