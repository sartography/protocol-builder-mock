import datetime
from datetime import date

import connexion
from flask import url_for, json, redirect, render_template, request, flash
from flask_migrate import Migrate

from flask_sqlalchemy import SQLAlchemy

PROTOCOLS = {}

def get_user_studies(user_id):
    return {"protocols": [p for p in PROTOCOLS.values() if p['user_id'] == user_id][:limit]}


def required_docs(id):
    return {
        'id': 21,
        'requirements': []
    }


def investigators(id):
    return

def get_protocol(id):
    return

def get_form(id, requirement_code):
    return


conn = connexion.App('Protocol Builder', specification_dir='./')
conn.add_api('api.yml')

app = conn.app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


@app.route("/site_map")
def site_map():
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    return json.dumps({"links": links})


app.config['SECRET_KEY'] = 'a really really really really long secret key'

from forms import StudyForm, StudySearchForm, StudyTable, InvestigatorForm
from models import Study, RequiredDocument, Investigator


@app.route('/', methods=['GET', 'POST'])
def index():
    # display results
    studies = db.session.query(Study).order_by(Study.last_updated.desc()).all()
    table = StudyTable(studies)
    return render_template('index.html', table=table)


@app.route('/new_study', methods=['GET', 'POST'])
def new_study():
    form = StudyForm(request.form)
    action = "/new_study"
    title = "New Study"
    if request.method == 'POST':
        study = Study()
        _update_study(study, form)
        flash('Study created successfully!')
        return redirect('/')

    return render_template('form.html', form=form)

@app.route('/study/<study_id>}', methods=['GET', 'POST'])
def edit_study(study_id):
    study = db.session.query(Study).filter(Study.study_id == study_id).first()
    form = StudyForm(request.form, obj=study)
    if request.method == 'GET':
        action = "/study/" + study_id
        title = "Edit Study #" + study_id
        if study.requirements:
            form.requirements.data = list(map(lambda r: r.code, list(study.requirements)))
        if study.q_complete:
            form.q_complete.checked = True
    if request.method == 'POST':
        _update_study(study, form)
        flash('Study updated successfully!')
        return redirect('/')
    return render_template('form.html', form=form)


@app.route('/investigator/<study_id>}', methods=['GET', 'POST'])
def new_investigator(study_id):
    form = InvestigatorForm(request.form)
    action = "/investigator/" + study_id
    title = "Add Investigator to Study " + study_id
    if request.method == 'POST':
        investigator = Investigator(study_id=study_id)
        investigator.netbadge_id = form.netbadge_id.data
        investigator.type = form.type.data
        investigator.description = form.type.label.text
        db.session.add(investigator)
        db.session.commit()
        flash('Investigator created successfully!')
        return redirect('/')

    return render_template('form.html', form=form)


@app.route('/del_investigator/<inv_id>}', methods=['GET'])
def del_investigator(inv_id):
    db.session.query(Investigator).filter(Investigator.id == inv_id).delete()
    db.session.commit()
    return redirect('/')


@app.route('/del_study/<study_id>}', methods=['GET'])
def del_study(study_id):
    db.session.query(Study).filter(Study.study_id == study_id).delete()
    db.session.commit()
    return redirect('/')


def _update_study(study, form):
    if study.study_id:
        db.session.query(RequiredDocument).filter(RequiredDocument.study_id == study.study_id).delete()
    for r in form.requirements:
        if r.checked:
            requirement = RequiredDocument(code=r.data, name=r.label.text, study=study)
            db.session.add(requirement)
    study.title = form.title.data
    study.netbadge_id = form.netbadge_id.data
    study.last_updated = datetime.datetime.now()
    study.q_complete = form.q_complete.data
    study.hsr_number = form.hsr_number.data
    db.session.add(study)
    db.session.commit()




if __name__ == '__main__':
    # run our standalone gevent server
    app.run(port=4200)