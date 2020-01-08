import connexion
from flask import url_for, json

PROTOCOLS = {}


def get_protocols(user_id):
    return {"protocols": [p for p in PROTOCOLS.values() if p['user_id'] == user_id][:limit]}


def get_protocol(id):
    return {
        id: 21,
        requirements: []
    }


def get_cover_sheet(id):
    return

def get_form(id):
    return

app = connexion.App('Protocol Builder', specification_dir='./')
app.add_api('api.yml')

application = app.app


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


@application.route("/")
def site_map():
    links = []
    for rule in application.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    return json.dumps({"links": links})

