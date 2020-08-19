import datetime
import os
import re
import yaml
from datetime import date

import connexion
from flask_cors import CORS
from flask import url_for, json, redirect, render_template, request, flash
from flask_assets import Environment, Bundle
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from sqlalchemy import func

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

connexion_app = connexion.FlaskApp('Protocol Builder', specification_dir='pb')
app = connexion_app.app

app.config.from_object('config.default')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if "TESTING" in os.environ and os.environ["TESTING"] == "true":
    app.config.from_object('config.testing')
    app.config.from_pyfile('config/testing.py')
else:
    app.config.root_path = app.instance_path
    app.config.from_pyfile('config.py', silent=True)

connexion_app.add_api('api.yml', base_path='/v2.0')

# Convert list of allowed origins to list of regexes
origins_re = [r"^https?:\/\/%s(.*)" % o.replace('.', '\.') for o in app.config['CORS_ALLOW_ORIGINS']]
cors = CORS(connexion_app.app, origins=origins_re)

db = SQLAlchemy(app)
""":type: sqlalchemy.orm.SQLAlchemy"""

session = db.session
""":type: sqlalchemy.orm.Session"""

migrate = Migrate(app, db)
ma = Marshmallow(app)

# Set the path of the static directory
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_STATIC = os.path.join(APP_ROOT, 'static')
BASE_HREF = app.config['APPLICATION_ROOT'].strip('/')
app.static_folder = APP_STATIC
app.static_url_path = app.config['APPLICATION_ROOT'] + 'static'

print('app.static_folder', app.static_folder)
print('app.static_url_path', app.static_url_path)

# remove old static map
url_map = app.url_map
try:
    for rule in url_map.iter_rules('static'):
        url_map._rules.remove(rule)
except ValueError:
    # no static view was created yet
    pass

# register new; the same view function is used
app.add_url_rule(
    app.static_url_path + '/<path:filename>',
    endpoint='static', view_func=app.send_static_file)

assets = Environment(app)
assets.init_app(app)
assets.url = app.static_url_path
scss = Bundle(
    'scss/app.scss',
    filters='pyscss',
    output='app.css'
)
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


@app.cli.command()
def load_example_data():
    """Load example data into the database."""
    from example_data import ExampleDataLoader
    ExampleDataLoader().clean_db()
    ExampleDataLoader().load_all()


@app.cli.command()
def load_example_sponsors():
    """Load example data into the database."""
    from example_data import ExampleDataLoader
    ExampleDataLoader().load_sponsors()


@app.route('/site_map')
def site_map():
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = app.confg['APPLICATION_ROOT'].strip('/') + url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    return json.dumps({"links": links})


# **************************
# WEB FORMS
# **************************
from pb.forms import StudyForm, StudyTable, InvestigatorForm, StudyDetailsForm, ConfirmDeleteForm, StudySponsorForm
from pb.models import Study, RequiredDocument, Investigator, StudySchema, RequiredDocumentSchema, InvestigatorSchema, \
    StudyDetails, StudyDetailsSchema, StudySponsor, Sponsor


@app.route('/', methods=['GET', 'POST'])
def index():
    # display results
    studies = db.session.query(Study).order_by(Study.DATE_MODIFIED.desc()).all()
    table = StudyTable(studies)
    return render_template(
        'index.html',
        table=table,
        base_href=BASE_HREF
    )


@app.route('/new_study', methods=['GET', 'POST'])
def new_study():
    form = StudyForm(request.form)
    action = BASE_HREF + "/new_study"
    title = "New Study"
    if request.method == 'POST':
        study = Study()
        study.study_details = StudyDetails()
        _update_study(study, form)
        flash('Study created successfully!', 'success')
        return redirect_home()

    return render_template(
        'form.html',
        form=form,
        action=action,
        title=title,
        description_map=description_map,
        base_href=BASE_HREF
    )


@app.route('/study/<study_id>', methods=['GET', 'POST'])
def edit_study(study_id):
    study = db.session.query(Study).filter(Study.STUDYID == study_id).first()
    form = StudyForm(request.form, obj=study)
    if request.method == 'GET':
        action = BASE_HREF + "/study/" + study_id
        title = "Edit Study #" + study_id
        if study.requirements:
            form.requirements.data = list(map(lambda r: r.AUXDOCID, list(study.requirements)))
        if study.Q_COMPLETE:
            form.Q_COMPLETE.checked = True
    if request.method == 'POST':
        _update_study(study, form)
        flash('Study updated successfully!', 'success')
        return redirect_home()
    return render_template(
        'form.html',
        form=form,
        action=action,
        title=title,
        description_map={},
        base_href=BASE_HREF
    )


@app.route('/investigator/<study_id>', methods=['GET', 'POST'])
def new_investigator(study_id):
    form = InvestigatorForm(request.form)

    # Remove options from form if unique investigator already exist, but AS_C and SI can happen many times.
    investigators = db.session.query(Investigator).filter(Investigator.STUDYID == study_id).all()
    choices = form.INVESTIGATORTYPE.choices
    existing_types = [i.INVESTIGATORTYPE for i in investigators]
    existing_types = list(filter(lambda a: a != "AS_C", existing_types))
    existing_types = list(filter(lambda a: a != "SI", existing_types))
    new_choices = [choice for choice in choices if choice[0] not in existing_types]
    form.INVESTIGATORTYPE.choices = new_choices

    action = BASE_HREF + "/investigator/" + study_id
    title = "Add Investigator to Study " + study_id
    if request.method == 'POST':
        investigator = Investigator(STUDYID=study_id)
        investigator.NETBADGEID = form.NETBADGEID.data
        investigator.set_type(form.INVESTIGATORTYPE.data)
        db.session.add(investigator)
        db.session.commit()
        flash('Investigator created successfully!', 'success')
        return redirect_home()

    return render_template(
        'form.html',
        form=form,
        action=action,
        title=title,
        description_map={},
        base_href=BASE_HREF
    )


@app.route('/del_investigator/<inv_id>', methods=['GET', 'POST'])
def del_investigator(inv_id):
    inv_id = int(inv_id)
    inv_model = db.session.query(Investigator).filter(Investigator.id == inv_id).first()
    if inv_model is None:
        flash('Investigator not found.', 'warn')
        return redirect_home()

    uid = inv_model.NETBADGEID
    study_id = int(inv_model.STUDYID)
    form = ConfirmDeleteForm(request.form, obj=inv_model)

    if request.method == 'GET':
        action = BASE_HREF + "/del_investigator/%i" % inv_id
        title = "Delete Investigator #%i?" % inv_id
        details = "Are you sure you want to delete Investigator '%s' from Study %i?" % (uid, study_id)

        return render_template(
            'form.html',
            form=form,
            action=action,
            title=title,
            details=details,
            description_map=description_map,
            base_href=BASE_HREF
        )

    if request.method == 'POST':
        if form.confirm and form.confirm.data:
            db.session.query(Investigator).filter(Investigator.id == inv_id).delete()
            db.session.commit()
            flash('Investigator %s deleted from Study %i.' % (uid, study_id), 'success')
        else:
            flash('Delete canceled.', 'info')

    return redirect_home()


@app.route('/study_sponsor/<study_id>', methods=['GET', 'POST'])
def edit_study_sponsor(study_id):
    study = db.session.query(Study).filter(Study.STUDYID == study_id).first()
    form = StudySponsorForm(request.form)
    action = BASE_HREF + "/study_sponsor/" + study_id
    title = "Edit sponsors for Study " + study_id
    form.SPONSOR_IDS.choices = [(s.SPONSOR_ID, f'{s.SP_NAME} ({s.SP_TYPE})') for s in db.session.query(Sponsor).all()]

    if request.method == 'GET':
        if hasattr(study, 'sponsors'):
            form.SPONSOR_IDS.data = [s.SPONSOR_ID for s in study.sponsors]

    if request.method == 'POST':
        # Remove all existing sponsors
        session.query(StudySponsor).filter(StudySponsor.SS_STUDY == study_id).delete()

        # Add the new ones
        for sponsor_id in form.SPONSOR_IDS.data:
            study_sponsor = StudySponsor(SS_STUDY=study_id, SPONSOR_ID=sponsor_id)
            db.session.add(study_sponsor)
            db.session.commit()

        sponsor_label = 'sponsor' if len(form.SPONSOR_IDS.data) == 1 else 'sponsors'
        flash(f'Study {sponsor_label} edited successfully!', 'success')
        return redirect_home()

    return render_template(
        'form.html',
        form=form,
        action=action,
        title=title,
        description_map={},
        base_href=BASE_HREF
    )


@app.route('/del_study_sponsor/<study_sponsor_id>', methods=['GET', 'POST'])
def del_study_sponsor(study_sponsor_id):
    study_sponsor_id = int(study_sponsor_id)
    study_sponsor_model: StudySponsor = db.session.query(StudySponsor).filter(StudySponsor.id == study_sponsor_id).first()

    if study_sponsor_model is None:
        flash('StudySponsor not found.', 'warn')
        return redirect_home()

    sponsor_span = f'<span class="highlight">{study_sponsor_model.sponsor.SP_NAME} ' \
                   f'({study_sponsor_model.sponsor.SP_TYPE})</span>'
    study_id = int(study_sponsor_model.SS_STUDY)
    form = ConfirmDeleteForm(request.form, obj=study_sponsor_model)

    if request.method == 'GET':
        action = f'{BASE_HREF}/del_study_sponsor/{study_sponsor_id}'
        title = 'Remove study sponsor?'
        details = f'Are you sure you want to remove {sponsor_span} ' \
                  f'as a sponsor of Study {study_id}? ' \
                  f'This will not remove the sponsor itself from the system.'

        return render_template(
            'form.html',
            form=form,
            action=action,
            title=title,
            details=details,
            description_map=description_map,
            base_href=BASE_HREF
        )

    if request.method == 'POST':
        if form.confirm and form.confirm.data:
            db.session.query(StudySponsor).filter(StudySponsor.id == study_sponsor_id).delete()
            db.session.commit()
            flash(f'Sponsor {sponsor_span} removed from Study {study_id}.', 'success')
        else:
            flash('Delete canceled.', 'info')

    return redirect_home()


@app.route('/del_study/<study_id>', methods=['GET', 'POST'])
def del_study(study_id):
    study_id = int(study_id)
    study_model = db.session.query(Study).filter(Study.STUDYID == study_id).first()
    if study_model is None:
        flash('Study not found.', 'warn')
        return redirect_home()

    form = ConfirmDeleteForm(request.form, obj=study_model)

    if request.method == 'GET':
        action = f'{BASE_HREF}/del_study/{study_id}'
        title = f'Delete Study #{study_id}?'
        details = f'Are you sure you want to delete Study <span class="highlight">{study_model.TITLE}</span>?'

        return render_template(
            'form.html',
            form=form,
            action=action,
            title=title,
            details=details,
            description_map=description_map,
            base_href=BASE_HREF
        )

    if request.method == 'POST':
        if form.confirm and form.confirm.data:
            db.session.query(RequiredDocument).filter(RequiredDocument.STUDYID == study_id).delete()
            db.session.query(Investigator).filter(Investigator.STUDYID == study_id).delete()
            db.session.query(StudyDetails).filter(StudyDetails.STUDYID == study_id).delete()
            db.session.query(StudySponsor).filter(StudySponsor.SS_STUDY == study_id).delete()
            study = db.session.query(Study).filter(Study.STUDYID == study_id).first()
            session.delete(study)
            db.session.commit()
            flash('Study %i deleted.' % study_id, 'success')
        else:
            flash('Delete canceled.', 'info')

        return redirect_home()


def _update_study(study, form):
    if study.STUDYID is None:
        # quick hack to get auto-increment without creating a bunch of hassle, this is not
        # production code by any stretch of the imagination, but this is a throw away library.
        max_id = db.session.query(func.max(Study.STUDYID)).scalar() or 1

        study.STUDYID = max_id + 1
    else:
        # Delete existing required documents for this study.
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
        action = BASE_HREF + "/study_details/" + study_id
        title = "Edit Study Details for Study #" + study_id
        details = "Numeric fields can be 1 for true, 0 or false, or Null if not applicable."
    if request.method == 'POST':
        form.populate_obj(study_details)
        db.session.add(study_details)
        db.session.commit()
        flash('Study updated successfully!', 'success')
        return redirect_home()
    return render_template(
        'form.html',
        form=form,
        action=action,
        title=title,
        details=details,
        description_map=description_map,
        base_href=BASE_HREF
    )


def redirect_home():
    return redirect(url_for('index'))


if __name__ == '__main__':
    # run our standalone gevent server
    app.run(port=4200)
