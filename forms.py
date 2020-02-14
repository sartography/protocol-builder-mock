from flask_table import Table, Col
from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, SubmitField, StringField, IntegerField

from app import db


class Study(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    requirements = db.relationship("RequiredDocument", backref="study", lazy='dynamic')


class RequiredDocument(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    active = db.Column(db.Boolean, default=False)
    study_id = db.Column(db.Integer, db.ForeignKey('study.id'))

    @staticmethod
    def all():
        docs = [RequiredDocument(id=1, name="Investigators Brochure"),
                RequiredDocument(id=6, name="Cancer Center's PRC Approval Form"),
                RequiredDocument(id=8, name="SOM CTO IND/IDE Review Letter"),
                RequiredDocument(id=9, name="HIRE Approval"),
                RequiredDocument(id=10, name="Cancer Center's PRC Approval Waiver"),
                RequiredDocument(id=12, name="Certificate of Confidentiality Application"),
                RequiredDocument(id=14, name="Institutional Biosafety Committee Approval"),
                RequiredDocument(id=18, name="SOM CTO Approval Letter - UVA PI Multisite Trial"),
                RequiredDocument(id=20,
                                 name="IRB Approval or Letter of Approval from Administration: Study Conducted at non- UVA Facilities "),
                RequiredDocument(id=21, name="New Medical Device Form"),
                RequiredDocument(id=22, name="SOM CTO Review regarding need for IDE"),
                RequiredDocument(id=23, name="SOM CTO Review regarding need for IND"),
                RequiredDocument(id=24, name="InfoSec Approval"),
                RequiredDocument(id=25, name="Scientific Pre-review Documentation"),
                RequiredDocument(id=26, name="IBC Number"),
                RequiredDocument(id=32, name="IDS - Investigational Drug Service Approval"),
                RequiredDocument(id=36, name="RDRC Approval "),
                RequiredDocument(id=40, name="SBS/IRB Approval-FERPA"),
                RequiredDocument(id=41, name="HIRE Standard Radiation Language"),
                RequiredDocument(id=42, name="COI Management Plan "),
                RequiredDocument(id=43, name="SOM CTO Approval Letter-Non UVA, Non Industry PI MultiSite Study"),
                RequiredDocument(id=44, name="GRIME Approval"),
                RequiredDocument(id=45, name="GMEC Approval"),
                RequiredDocument(id=46, name="IRB Reliance Agreement Request Form- IRB-HSR is IRB of Record"),
                RequiredDocument(id=47, name="Non UVA IRB Approval - Initial and Last Continuation"),
                RequiredDocument(id=48, name="MR Physicist Approval- Use of Gadolinium"),
                RequiredDocument(id=49, name="SOM CTO Approval- Non- UVA Academia PI of IDE"),
                RequiredDocument(id=51, name="IDS Waiver"),
                RequiredDocument(id=52, name="Package Inserts"),
                RequiredDocument(id=53, name="IRB Reliance Agreement Request Form- IRB-HSR Not IRB of Record"),
                RequiredDocument(id=54, name="ESCRO Approval"),
                RequiredDocument(id=57, name="Laser Safety Officer Approval")]
        return docs


class StudySearchForm(FlaskForm):
    search = StringField('')


class StudyForm(FlaskForm):
    id = IntegerField('Study Id')
    title = StringField('Title')
    requirements = SelectMultipleField("Requirements", choices=[(rd.id, rd.name) for rd in RequiredDocument.all()])

class StudyTable(Table):
    id = Col('Id')
    title = Col('Artist')
    requirements = Col('Title')
