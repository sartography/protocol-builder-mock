import os
import yaml

import connexion
from flask_cors import CORS
from flask_assets import Environment, Bundle
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

PROTOCOLS = {}


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

# Convert list of allowed origins to list of regexes
origins_re = [r"^https?:\/\/%s(.*)" % o.replace('.', '\.') for o in app.config['CORS_ALLOW_ORIGINS']]
cors = CORS(connexion_app.app, origins=origins_re)

db = SQLAlchemy(app)
""":type: sqlalchemy.orm.SQLAlchemy"""

session = db.session
""":type: sqlalchemy.orm.Session"""

migrate = Migrate(app, db)
ma = Marshmallow(app)

connexion_app.add_api('api.yml', base_path='/v2.0')

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
# LOAD ROUTES
# **************************
import pb.routes


# **************************
# FLASK COMMANDS
# **************************

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


if __name__ == '__main__':
    # run our standalone gevent server
    app.run(port=4200)
