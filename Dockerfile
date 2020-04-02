FROM python:3.7

ENV PATH=/root/.local/bin:/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin

# install node and yarn
RUN apt-get update
RUN apt-get -y install postgresql-client libpcre3 libpcre3-dev

# config project dir
RUN mkdir /protocol-builder-mock
WORKDIR /protocol-builder-mock

# install python requirements
RUN pip install pipenv
ADD Pipfile /protocol-builder-mock/
ADD Pipfile.lock /protocol-builder-mock/
RUN pipenv install --dev


# include rejoiner code (gets overriden by local changes)
COPY . /protocol-builder-mock/

ENV FLASK_APP=/protocol-builder-mock/app.py

# run webserver by default
CMD ["pipenv", "run", "flask", "db", "upgrade"]
CMD ["pipenv", "run", "python", "./run.py"]


# expose ports
EXPOSE 6000


