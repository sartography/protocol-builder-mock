FROM python:3.7-slim

WORKDIR /app
COPY Pipfile Pipfile.lock /app/

RUN set -xe \
  && pip install pipenv \
  && apt-get update -q \
  && apt-get install -y -q \
        gcc python3-dev libssl-dev \
        curl postgresql-client git-core \
        gunicorn3 postgresql-client \
  && pipenv install --dev \
  && apt-get remove -y gcc python3-dev libssl-dev \
  && apt-get autoremove -y \
  && apt-get clean -y \
  && rm -rf /var/lib/apt/lists/* \
  && mkdir -p /app \
  && useradd _gunicorn --no-create-home --user-group

COPY . /app/
WORKDIR /app
ENV FLASK_APP=/app/pb/__init__.py

# Don't run gunicorn until the DC/OS container actually starts.
# Otherwise, environment variables will not be available.
#CMD ["pipenv", "run", "gunicorn", \
#     "--bind", "0.0.0.0:8000", \
#     "-e", "SCRIPT_NAME=/api", \
#     "wsgi:app"]
