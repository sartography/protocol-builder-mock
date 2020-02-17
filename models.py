from sqlalchemy import func
from app import db


class Study(db.Model):
    study_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    netbadge_id = db.Column(db.String(), nullable=False)
    requirements = db.relationship("RequiredDocument", backref="study", lazy='dynamic')
    investigators = db.relationship("Investigator", backref="study", lazy='dynamic')
    last_updated = db.Column(db.DateTime(timezone=True), default=func.now())
    hsr_number = db.Column(db.String())
    q_complete = db.Column(db.Boolean, nullable=True)


class Investigator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    study_id = db.Column(db.Integer, db.ForeignKey('study.study_id'))
    netbadge_id = db.Column(db.String(), nullable=False)
    type = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)

    @staticmethod
    def all_types():
        types = [
            Investigator(type="PI", description="Primary Investigator"),
            Investigator(type="SI", description="Sub Investigator"),
            Investigator(type="DC", description="Department Contact"),
            Investigator(type="SC_I", description="Study Coordinator 1"),
            Investigator(type="SC_II", description="Study Coordinator 2"),
            Investigator(type="AS_C", description="Additional Study Coordinators"),
            Investigator(type="DEPT_CH", description="Department Chair"),
            Investigator(type="IRBC", description="IRB Coordinator"),
            Investigator(type="SCI", description="Scientific Contact"),
        ]
        return types


class RequiredDocument(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(), nullable=False, default="")
    name = db.Column(db.String(), nullable=False, default="")
    study_id = db.Column(db.Integer, db.ForeignKey('study.study_id'))

    @staticmethod
    def all():
        docs = [RequiredDocument(code=1, name="Investigators Brochure"),
                RequiredDocument(code=6, name="Cancer Center's PRC Approval Form"),
                RequiredDocument(code=8, name="SOM CTO IND/IDE Review Letter"),
                RequiredDocument(code=9, name="HIRE Approval"),
                RequiredDocument(code=10, name="Cancer Center's PRC Approval Waiver"),
                RequiredDocument(code=12, name="Certificate of Confidentiality Application"),
                RequiredDocument(code=14, name="Institutional Biosafety Committee Approval"),
                RequiredDocument(code=18, name="SOM CTO Approval Letter - UVA PI Multisite Trial"),
                RequiredDocument(code=20,
                                 name="IRB Approval or Letter of Approval from Administration: Study Conducted at non- UVA Facilities "),
                RequiredDocument(code=21, name="New Medical Device Form"),
                RequiredDocument(code=22, name="SOM CTO Review regarding need for IDE"),
                RequiredDocument(code=23, name="SOM CTO Review regarding need for IND"),
                RequiredDocument(code=24, name="InfoSec Approval"),
                RequiredDocument(code=25, name="Scientific Pre-review Documentation"),
                RequiredDocument(code=26, name="IBC Number"),
                RequiredDocument(code=32, name="IDS - Investigational Drug Service Approval"),
                RequiredDocument(code=36, name="RDRC Approval "),
                RequiredDocument(code=40, name="SBS/IRB Approval-FERPA"),
                RequiredDocument(code=41, name="HIRE Standard Radiation Language"),
                RequiredDocument(code=42, name="COI Management Plan "),
                RequiredDocument(code=43, name="SOM CTO Approval Letter-Non UVA, Non Industry PI MultiSite Study"),
                RequiredDocument(code=44, name="GRIME Approval"),
                RequiredDocument(code=45, name="GMEC Approval"),
                RequiredDocument(code=46, name="IRB Reliance Agreement Request Form- IRB-HSR is IRB of Record"),
                RequiredDocument(code=47, name="Non UVA IRB Approval - Initial and Last Continuation"),
                RequiredDocument(code=48, name="MR Physicist Approval- Use of Gadolinium"),
                RequiredDocument(code=49, name="SOM CTO Approval- Non- UVA Academia PI of IDE"),
                RequiredDocument(code=51, name="IDS Waiver"),
                RequiredDocument(code=52, name="Package Inserts"),
                RequiredDocument(code=53, name="IRB Reliance Agreement Request Form- IRB-HSR Not IRB of Record"),
                RequiredDocument(code=54, name="ESCRO Approval"),
                RequiredDocument(code=57, name="Laser Safety Officer Approval")]
        return docs
