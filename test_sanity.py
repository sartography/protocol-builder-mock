import os

os.environ["TESTING"] = "true"

import unittest
from app import app, db
from forms import StudyForm
from models import Study, RequiredDocument


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

    def test_add_and_edit_study(self):
        """Add and edit a study"""
        study = Study(TITLE="My Test Document", NETBADGEID="dhf8r")
        form = StudyForm(formdata=None, obj=study)
        num_reqs = len(form.requirements.choices)
        self.assertGreater(num_reqs, 0)

        for r in form.requirements:
            form.data['requirements'].append(r.data)

        r = self.app.post('/new_study', data=form.data, follow_redirects=True)
        assert r.status_code == 200
        added_study = Study.query.filter(Study.TITLE == "My Test Document").first()
        assert added_study
        num_studies_before = Study.query.count()

        num_docs_before = RequiredDocument.query.filter(Study.STUDYID == added_study.STUDYID).count()
        self.assertEqual(num_reqs, num_docs_before)

        """Edit an existing study"""
        added_study.title = "New Title"
        form_2 = StudyForm(formdata=None, obj=added_study)

        for r in form_2.requirements:
            form_2.data['requirements'].append(r.data)

        r_2 = self.app.post('/study/%i' % added_study.STUDYID, data=form_2.data, follow_redirects=True)
        assert r_2.status_code == 200
        num_studies_after = Study.query.count()
        edited_study = Study.query.filter(Study.STUDYID == added_study.STUDYID).first()
        assert edited_study

        num_docs_after = RequiredDocument.query.filter(Study.STUDYID == edited_study.STUDYID).count()
        self.assertEqual(num_docs_before, num_docs_after)
        self.assertEqual(num_studies_before, num_studies_after)
