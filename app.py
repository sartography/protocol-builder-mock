import connexion
from flask import url_for, json

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


if __name__ == '__main__':
    # run our standalone gevent server
    app.run(port=4200)