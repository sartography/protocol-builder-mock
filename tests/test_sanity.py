import os
import json

from werkzeug.datastructures import MultiDict

os.environ["TESTING"] = "true"

import unittest
import random
import string
from pb import app, db, session
from pb.forms import StudyForm, StudySponsorForm
from pb.ldap.ldap_service import LdapService
from pb.models import Study, RequiredDocument, Sponsor, StudySponsor
from example_data import ExampleDataLoader

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

    def setUp(self):
        ExampleDataLoader().clean_db()
        self.ctx.push()

    def tearDown(self):
        ExampleDataLoader().clean_db()
        self.ctx.pop()
        self.auths = {}

    def load_sponsors(self):
        ExampleDataLoader().load_sponsors()
        sponsors = session.query(Sponsor).all()
        num_lines = sum(1 for line in open('pb/static/csv/sponsors.csv'))
        self.assertIsNotNone(sponsors)
        self.assertEqual(len(sponsors), num_lines - 1)
        return sponsors

    def add_study(self, title=None):
        if title is None:
            study_title = "My Test Document" + ''.join(random.choices(string.digits, k=8))
        else:
            study_title = title
        study = Study(TITLE=study_title, NETBADGEID="dhf8r")
        form = StudyForm(formdata=None, obj=study)
        num_reqs = len(form.requirements.choices)
        self.assertGreater(num_reqs, 0)

        for r in form.requirements:
            form.data['requirements'].append(r.data)

        r = self.app.post('/new_study', data=form.data, follow_redirects=False)
        assert r.status_code == 302
        added_study = Study.query.filter(Study.TITLE == study_title).first()
        assert added_study

        num_docs_before = RequiredDocument.query.filter(Study.STUDYID == added_study.STUDYID).count()
        self.assertEqual(num_reqs, num_docs_before)

        return added_study

    def test_add_and_edit_study(self):
        """Add and edit a study"""
        added_study: Study = self.add_study()
        num_studies_before = Study.query.count()
        num_docs_before = RequiredDocument.query.filter(Study.STUDYID == added_study.STUDYID).count()

        """Edit an existing study"""
        added_study.title = "New Title" + ''.join(random.choices(string.digits, k=8))
        form_2 = StudyForm(formdata=None, obj=added_study)

        for r in form_2.requirements:
            form_2.data['requirements'].append(r.data)

        r_2 = self.app.post('/study/%i' % added_study.STUDYID, data=form_2.data, follow_redirects=False)
        assert r_2.status_code == 302
        num_studies_after = Study.query.count()
        edited_study = Study.query.filter(Study.STUDYID == added_study.STUDYID).first()
        assert edited_study

        num_docs_after = RequiredDocument.query.filter(Study.STUDYID == edited_study.STUDYID).count()
        self.assertEqual(num_docs_before, num_docs_after)
        self.assertEqual(num_studies_before, num_studies_after)

    def test_add_sponsors(self):
        """Load sponsors twice in a row to make sure duplicates aren't created."""
        self.load_sponsors()
        self.load_sponsors()


    def test_add_and_edit_study_sponsor(self):
        """Add and edit a study sponsor"""
        num_sponsors = 5
        all_sponsors = self.load_sponsors()
        study: Study = self.add_study()
        self.assertIsNotNone(study)

        num_study_sponsors_before = len(study.sponsors)
        self.assertEqual(num_study_sponsors_before, 0)

        study_sponsors_before = session.query(StudySponsor).filter(StudySponsor.SS_STUDY == study.STUDYID).all()
        self.assertEqual(len(study_sponsors_before), 0)

        """Add sponsors to an existing study"""
        random_sponsor_ids = random.choices([s.SPONSOR_ID for s in all_sponsors], k=num_sponsors)
        self.assertEqual(len(random_sponsor_ids), num_sponsors)
        formdata = MultiDict()
        formdata.add('SS_STUDY', study.STUDYID)

        for sponsor_id in random_sponsor_ids:
            formdata.add('SPONSOR_IDS', sponsor_id)

        form = StudySponsorForm(formdata=formdata, obj=study)
        form.SPONSOR_IDS.choices = [(s.SPONSOR_ID, f'{s.SP_NAME} ({s.SP_TYPE})') for s in all_sponsors]
        self.assertEqual(len(form.data['SPONSOR_IDS']), num_sponsors)

        rv = self.app.post(f'/study_sponsor/{study.STUDYID}', data=form.data, follow_redirects=False)
        assert rv.status_code == 302
        edited_study = Study.query.filter(Study.STUDYID == study.STUDYID).first()
        assert edited_study

        num_study_sponsors_after = len(edited_study.sponsors)
        self.assertGreater(num_study_sponsors_after, 0)
        self.assertEqual(num_study_sponsors_after, num_sponsors)

        study_sponsors_after = session.query(StudySponsor).filter(StudySponsor.SS_STUDY == study.STUDYID).all()
        self.assertGreater(len(study_sponsors_after), 0)
        self.assertEqual(len(study_sponsors_after), num_sponsors)

    def test_ldap_search(self):
        needle = 'funk'
        result = LdapService.users_as_json(needle)
        users = json.loads(result)
        print(f'len of users: {len(users)}')
        # self.assertEqual(2, len(users))
        uids = []
        for user in users:
            uids.append(user['uid'])
        self.assertIn('dhf8r', uids)


    def test_user_studies(self):
        studies1 = self.app.get(f'/user_studies')
        self.assertEqual('308 PERMANENT REDIRECT', studies1.status)
        for header in studies1.headers:
            if header[0] == 'Location':
                self.assertIn('user_studies', header[1])
        studies2 = self.app.get(f'/user_studies/')
        self.assertEqual('302 FOUND', studies2.status)
        for header in studies2.headers:
            if header[0] == 'Location':
                self.assertNotIn('user_studies', header[1])

    def test_long_study_name(self):
        title = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla egestas quam id ullamcorper facilisis. Praesent ultricies urna malesuada velit ultricies efficitur. Nam eu eleifend libero. Mauris ac erat augue. Curabitur ac fringilla tellus. Morbi sem quam, consectetur sit amet eros non, semper congue metus. Sed sollicitudin augue eu justo fermentum volutpat at sit amet metus. Vestibulum hendrerit pharetra ante. Sed porttitor diam nibh, quis elementum est placerat sit amet. Phasellus magna libero, porta quis euismod et, commodo eu nisl. Quisque consectetur sagittis interdum. Nullam congue consectetur elementum. In hac habitasse platea dictumst. Duis placerat iaculis odio, ac faucibus felis vehicula nec. Praesent cursus id turpis ac maximus.'
        study = self.add_study(title=title)
        self.assertEqual(title, study.TITLE)

    # def test_study_details_validation(self):
    #
    #     test_study = self.add_study()
    #     data = {'IS_IND': 1, 'IND_1': 1234}
    #     r = self.app.post(f'/study_details/{test_study.STUDYID}', data=data, follow_redirects=False)
    #     self.assertNotIn('Form did not validate!', r.data.decode('utf-8'))
    #
    #     print('test_study_details_validation')
    #
    # def test_study_details_validation_fail(self):
    #     test_study = self.add_study()
    #     data = {'IS_IND': 1, 'IND_1': 1234, 'IS_IDE': 'b'}
    #     r = self.app.post(f'/study_details/{test_study.STUDYID}', data=data, follow_redirects=False)
    #     self.assertIn('Form did not validate!', r.data.decode('utf-8'))
    #
    #     print('test_study_details_validation_fail')
