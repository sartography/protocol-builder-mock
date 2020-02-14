import connexion
from flask import url_for, json, redirect, render_template, request, flash

from flask_sqlalchemy import SQLAlchemy

PROTOCOLS = {}


def get_user_studies(user_id):
    return {"protocols": [p for p in PROTOCOLS.values() if p['user_id'] == user_id][:limit]}


def required_docs(id):
    return {
        id: 21,
        requirements: []
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

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

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

from forms import Study, StudyForm, StudySearchForm, StudyTable, RequiredDocument

@app.route('/', methods=['GET', 'POST'])
def index():
    search = StudySearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
    return render_template('index.html', form=search)


@app.route('/results')
def search_results(search):
    results = []
    search_string = search.data['search']
    if search.data['search'] == '':
        qry = db.session.query(Study)
        results = qry.all()
    if not results:
        flash('No results found!')
        return redirect('/')
    else:
        # display results
        studies = db.session.query("Study").all()
        table = StudyTable(studies)
        return render_template('results.html', table=table)


@app.route('/new_study', methods=['GET', 'POST'])
def new_study():
    form = StudyForm(request.form)
    if request.method == 'POST':
        # save the study
        study = Study()
        study.id = form.id
        study.title = form.title
#        for r in form.requirements:
#            requirement = RequiredDocument(id = r.id,
#        study.requirements = form.requirements
        db.session.add(study)
        db.session.commit()
        flash('Album created successfully!')
        return redirect('/')

    form = StudyForm(request.form)
    return render_template('study_form.html', form=form)


if __name__ == '__main__':
    # run our standalone gevent server
    app.run(port=4200)