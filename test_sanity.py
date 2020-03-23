import json
import os
os.environ["TESTING"] = "true"

import unittest
from app import app, db
from forms import StudyForm
from models import Study


class Sanity_Check_Test(unittest.TestCase):

    auths = {}

    @classmethod
    def setUpClass(cls):
        cls.ctx = app.test_request_context()
        cls.app = app.test_client()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        db.drop_all()
        db.session.remove()
        pass

    def setUp(self):
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()
        self.auths = {}

    def test_add_study_post(self):
        """Does add study post a new study?"""
        study = Study(TITLE="My Test Document", NETBADGEID="dhf8r")
        form = StudyForm(formdata=None, obj=study)
        r = self.app.post('/new_study', data=form.data, follow_redirects=True)
        assert r.status_code == 200
        added_study = Study.query.filter(
            Study.TITLE == "My Test Document").first()
        assert added_study

