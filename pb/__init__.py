import datetime
import os
import re
from datetime import date

import connexion
import yaml
from flask import url_for, json, redirect, render_template, request, flash
from flask_assets import Environment, Bundle
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from sqlalchemy import func
from wtforms.ext.appengine.db import model_form

PROTOCOLS = {}


def get_user_studies(uva_id):
    studies = db.session.query(Study).filter(Study.NETBADGEID == uva_id).all()
    return StudySchema(many=True).dump(studies)


def required_docs(studyid):
    docs = db.session.query(RequiredDocument).filter(RequiredDocument.STUDYID == studyid).all()
    return RequiredDocumentSchema(many=True).dump(docs)


def investigators(studyid):
    inv = db.session.query(Investigator).filter(Investigator.STUDYID == studyid).all()
    return InvestigatorSchema(many=True).dump(inv)


def get_study_details(studyid):
    details = db.session.query(StudyDetails).filter(StudyDetails.STUDYID == studyid).first()
    return StudyDetailsSchema().dump(details)


def get_form(id, requirement_code):
    return

conn = connexion.App('Protocol Builder', specification_dir='pb')

app = conn.app

app.config.from_object('config.default')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if "TESTING" in os.environ and os.environ["TESTING"] == "true":
    app.config.from_object('config.testing')
    app.config.from_pyfile('config/testing.py')
else:
    app.config.root_path = app.instance_path
    app.config.from_pyfile('config.py', silent=True)

conn.add_api('api.yml', base_path='/pb')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)
assets = Environment(app)
assets.url = app.static_url_path
scss = Bundle('scss/app.scss', filters='pyscss', output='app.css')
assets.register('app_scss', scss)

# Loads all the descriptions from the API so we can display them in the editor.
description_map = {}
with open(r'pb/api.yml') as file:
    api_config = yaml.load(file, Loader=yaml.FullLoader)
    study_detail_properties = api_config['components']['schemas']['StudyDetail']['properties']
    for schema in api_config['components']['schemas']:
        for field, values in api_config['components']['schemas'][schema]['properties'].items():
            description_map[field] = values['description']


# **************************
# API ENDPOINTS
# **************************
def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


@app.route('/site_map')
def site_map():
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    return json.dumps({"links": links})


# **************************
# WEB FORMS
# **************************
from pb.forms import StudyForm, StudyTable, InvestigatorForm, StudyDetailsForm
from pb.models import Study, RequiredDocument, Investigator, StudySchema, RequiredDocumentSchema, InvestigatorSchema, \
    StudyDetails, StudyDetailsSchema


@app.route('/', methods=['GET', 'POST'])
def index():
    # display results
    studies = db.session.query(Study).order_by(Study.DATE_MODIFIED.desc()).all()
    table = StudyTable(studies)
    return render_template('index.html', table=table, APPLICATION_ROOT=app.config['APPLICATION_ROOT'])


@app.route('/new_study', methods=['GET', 'POST'])
def new_study():
    form = StudyForm(request.form)
    action = "/new_study"
    title = "New Study"
    if request.method == 'POST':
        study = Study()
        study.study_details = StudyDetails()
        _update_study(study, form)
        flash('Study created successfully!')
        return redirect('/')

    return render_template('form.html', form=form,
                           action=action,
                           title=title,
                           description_map=description_map)


@app.route('/study/<study_id>', methods=['GET', 'POST'])
def edit_study(study_id):
    study = db.session.query(Study).filter(Study.STUDYID == study_id).first()
    form = StudyForm(request.form, obj=study)
    if request.method == 'GET':
        action = "/study/" + study_id
        title = "Edit Study #" + study_id
        if study.requirements:
            form.requirements.data = list(map(lambda r: r.AUXDOCID, list(study.requirements)))
        if study.Q_COMPLETE:
            form.Q_COMPLETE.checked = True
    if request.method == 'POST':
        _update_study(study, form)
        flash('Study updated successfully!')
        return redirect('/')
    return render_template('form.html', form=form,
                           action=action,
                           title=title,
                           description_map={})


@app.route('/investigator/<study_id>', methods=['GET', 'POST'])
def new_investigator(study_id):
    form = InvestigatorForm(request.form)
    action = "/investigator/" + study_id
    title = "Add Investigator to Study " + study_id
    if request.method == 'POST':
        investigator = Investigator(STUDYID=study_id)
        investigator.NETBADGEID = form.NETBADGEID.data
        investigator.set_type(form.INVESTIGATORTYPE.data)
        db.session.add(investigator)
        db.session.commit()
        flash('Investigator created successfully!')
        return redirect('/')

    return render_template('form.html', form=form,
                           action=action,
                           title=title,
                           description_map={})


@app.route('/del_investigator/<inv_id>', methods=['GET'])
def del_investigator(inv_id):
    db.session.query(Investigator).filter(Investigator.id == inv_id).delete()
    db.session.commit()
    return redirect('/')


@app.route('/del_study/<study_id>', methods=['GET'])
def del_study(study_id):
    db.session.query(RequiredDocument).filter(RequiredDocument.STUDYID == study_id).delete()
    db.session.query(Investigator).filter(Investigator.STUDYID == study_id).delete()
    db.session.query(StudyDetails).filter(StudyDetails.STUDYID == study_id).delete()
    db.session.query(Study).filter(Study.STUDYID == study_id).delete()
    db.session.commit()
    return redirect('/')


def _update_study(study, form):
    if study.STUDYID is None:
        # quick hack to get auto-increment without creating a bunch of hassle, this is not
        # production code by any stretch of the imagination, but this is a throw away library.
        max_id = db.session.query(func.max(Study.STUDYID)).scalar() or 1

        study.STUDYID = max_id + 1
    else:
        db.session.query(RequiredDocument).filter(RequiredDocument.STUDYID == study.STUDYID).delete()

    study.TITLE = form.TITLE.data
    study.NETBADGEID = form.NETBADGEID.data
    study.DATE_MODIFIED = datetime.datetime.now()
    study.Q_COMPLETE = form.Q_COMPLETE.data
    study.HSRNUMBER = form.HSRNUMBER.data

    for r in form.requirements:
        if r.checked:
            requirement = RequiredDocument(AUXDOCID=r.data, AUXDOC=r.label.text, study=study)
            db.session.add(requirement)

    db.session.add(study)
    db.session.commit()


@app.route('/study_details/<study_id>', methods=['GET', 'POST'])
def study_details(study_id):
    study_details = db.session.query(StudyDetails).filter(StudyDetails.STUDYID == study_id).first()
    if not study_details:
        study_details = StudyDetails(STUDYID=study_id)
    form = StudyDetailsForm(request.form, obj=study_details)
    if request.method == 'GET':
        action = "/study_details/" + study_id
        title = "Edit Study Details for Study #" + study_id
        details = "Numeric fields can be 1 for true, 0 or false, or Null if not applicable."
    if request.method == 'POST':
        form.populate_obj(study_details)
        db.session.add(study_details)
        db.session.commit()
        flash('Study updated successfully!')
        return redirect('/')
    return render_template('form.html', form=form,
                           action=action,
                           title=title,
                           details=details,
                           description_map=description_map)


if __name__ == '__main__':
    # run our standalone gevent server
    app.run(port=4200)
