from sqlalchemy import func
from app import db, ma


class Study(db.Model):
    STUDYID = db.Column(db.Integer, primary_key=True)
    HSRNUMBER = db.Column(db.String())
    TITLE = db.Column(db.String(80), nullable=False)
    NETBADGEID = db.Column(db.String(), nullable=False)
    Q_COMPLETE = db.Column(db.Boolean, nullable=True)
    DATE_MODIFIED = db.Column(db.DateTime(timezone=True), default=func.now())
    requirements = db.relationship("RequiredDocument", backref="study", lazy='dynamic')
    investigators = db.relationship("Investigator", backref="study", lazy='dynamic')
    study_details = db.relationship("StudyDetails", uselist=False, backref="study")

class StudySchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("STUDYID", "HSRNUMBER", "TITLE", "NETBADGEID",
                  "Q_COMPLETE", "DATE_MODIFIED")


class Investigator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    STUDYID = db.Column(db.Integer, db.ForeignKey('study.STUDYID'))
    NETBADGEID = db.Column(db.String(), nullable=False)
    INVESTIGATORTYPE = db.Column(db.String(), nullable=False)
    INVESTIGATORTYPEFULL = db.Column(db.String(), nullable=False)

    @staticmethod
    def all_types():
        types = [
            Investigator(INVESTIGATORTYPE="PI", INVESTIGATORTYPEFULL="Primary Investigator"),
            Investigator(INVESTIGATORTYPE="SI", INVESTIGATORTYPEFULL="Sub Investigator"),
            Investigator(INVESTIGATORTYPE="DC", INVESTIGATORTYPEFULL="Department Contact"),
            Investigator(INVESTIGATORTYPE="SC_I", INVESTIGATORTYPEFULL="Study Coordinator 1"),
            Investigator(INVESTIGATORTYPE="SC_II", INVESTIGATORTYPEFULL="Study Coordinator 2"),
            Investigator(INVESTIGATORTYPE="AS_C", INVESTIGATORTYPEFULL="Additional Study Coordinators"),
            Investigator(INVESTIGATORTYPE="DEPT_CH", INVESTIGATORTYPEFULL="Department Chair"),
            Investigator(INVESTIGATORTYPE="IRBC", INVESTIGATORTYPEFULL="IRB Coordinator"),
            Investigator(INVESTIGATORTYPE="SCI", INVESTIGATORTYPEFULL="Scientific Contact"),
        ]
        return types

    def set_type(self, type_code):
        self.INVESTIGATORTYPE = type_code
        for t in self.all_types():
            if t.INVESTIGATORTYPE == type_code:
                self.INVESTIGATORTYPEFULL = t.INVESTIGATORTYPEFULL

class InvestigatorSchema(ma.Schema):
    class Meta:
        fields = ("NETBADGEID", "INVESTIGATORTYPE", "INVESTIGATORTYPEFULL")


class RequiredDocument(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    AUXDOCID = db.Column(db.String(), nullable=False, default="")
    AUXDOC = db.Column(db.String(), nullable=False, default="")
    STUDYID = db.Column(db.Integer, db.ForeignKey('study.STUDYID'))

    @staticmethod
    def all():
        docs = [RequiredDocument(AUXDOCID=1, AUXDOC="Investigators Brochure"),
                RequiredDocument(AUXDOCID=6, AUXDOC="Cancer Center's PRC Approval Form"),
                RequiredDocument(AUXDOCID=8, AUXDOC="SOM CTO IND/IDE Review Letter"),
                RequiredDocument(AUXDOCID=9, AUXDOC="HIRE Approval"),
                RequiredDocument(AUXDOCID=10, AUXDOC="Cancer Center's PRC Approval Waiver"),
                RequiredDocument(AUXDOCID=12, AUXDOC="Certificate of Confidentiality Application"),
                RequiredDocument(AUXDOCID=14, AUXDOC="Institutional Biosafety Committee Approval"),
                RequiredDocument(AUXDOCID=18, AUXDOC="SOM CTO Approval Letter - UVA PI Multisite Trial"),
                RequiredDocument(AUXDOCID=20,
                                 AUXDOC="IRB Approval or Letter of Approval from Administration: Study Conducted at non- UVA Facilities "),
                RequiredDocument(AUXDOCID=21, AUXDOC="New Medical Device Form"),
                RequiredDocument(AUXDOCID=22, AUXDOC="SOM CTO Review regarding need for IDE"),
                RequiredDocument(AUXDOCID=23, AUXDOC="SOM CTO Review regarding need for IND"),
                RequiredDocument(AUXDOCID=24, AUXDOC="InfoSec Approval"),
                RequiredDocument(AUXDOCID=25, AUXDOC="Scientific Pre-review Documentation"),
                RequiredDocument(AUXDOCID=26, AUXDOC="IBC Number"),
                RequiredDocument(AUXDOCID=32, AUXDOC="IDS - Investigational Drug Service Approval"),
                RequiredDocument(AUXDOCID=33, AUXDOC="Data Security Plan"),
                RequiredDocument(AUXDOCID=36, AUXDOC="RDRC Approval "),
                RequiredDocument(AUXDOCID=40, AUXDOC="SBS/IRB Approval-FERPA"),
                RequiredDocument(AUXDOCID=41, AUXDOC="HIRE Standard Radiation Language"),
                RequiredDocument(AUXDOCID=42, AUXDOC="COI Management Plan "),
                RequiredDocument(AUXDOCID=43, AUXDOC="SOM CTO Approval Letter-Non UVA, Non Industry PI MultiSite Study"),
                RequiredDocument(AUXDOCID=44, AUXDOC="GRIME Approval"),
                RequiredDocument(AUXDOCID=45, AUXDOC="GMEC Approval"),
                RequiredDocument(AUXDOCID=46, AUXDOC="IRB Reliance Agreement Request Form- IRB-HSR is IRB of Record"),
                RequiredDocument(AUXDOCID=47, AUXDOC="Non UVA IRB Approval - Initial and Last Continuation"),
                RequiredDocument(AUXDOCID=48, AUXDOC="MR Physicist Approval- Use of Gadolinium"),
                RequiredDocument(AUXDOCID=49, AUXDOC="SOM CTO Approval- Non- UVA Academia PI of IDE"),
                RequiredDocument(AUXDOCID=51, AUXDOC="IDS Waiver"),
                RequiredDocument(AUXDOCID=52, AUXDOC="Package Inserts"),
                RequiredDocument(AUXDOCID=53, AUXDOC="IRB Reliance Agreement Request Form- IRB-HSR Not IRB of Record"),
                RequiredDocument(AUXDOCID=54, AUXDOC="ESCRO Approval"),
                RequiredDocument(AUXDOCID=57, AUXDOC="Laser Safety Officer Approval")]
        return docs


class RequiredDocumentSchema(ma.Schema):
    class Meta:
        fields = ("AUXDOCID", "AUXDOC")


class StudyDetails(db.Model):
    STUDYID = db.Column(db.Integer, db.ForeignKey('study.STUDYID'), primary_key=True)
    IS_IND = db.Column(db.Integer, nullable=True)
    IND_1 = db.Column(db.String, nullable=True)
    IND_2 = db.Column(db.String, nullable=True)
    IND_3 = db.Column(db.String, nullable=True)
    IS_UVA_IND = db.Column(db.Integer, nullable=True)
    IS_IDE = db.Column(db.Integer, nullable=True)
    IS_UVA_IDE = db.Column(db.Integer, nullable=True)
    IDE = db.Column(db.String, nullable=True)
    IS_CHART_REVIEW = db.Column(db.Integer, nullable=True)
    IS_RADIATION = db.Column(db.Integer, nullable=True)
    GCRC_NUMBER = db.Column(db.String, nullable=True)
    IS_GCRC = db.Column(db.Integer, nullable=True)
    IS_PRC_DSMP = db.Column(db.Integer, nullable=True)
    IS_PRC = db.Column(db.Integer, nullable=True)
    PRC_NUMBER = db.Column(db.String, nullable=True)
    IS_IBC = db.Column(db.Integer, nullable=True)
    IBC_NUMBER = db.Column(db.String, nullable=True)
    SPONSORS_PROTOCOL_REVISION_DATE = db.Column(db.Integer, nullable=True)
    IS_SPONSOR_MONITORING = db.Column(db.Integer, nullable=True)
    IS_AUX  = db.Column(db.Integer, nullable=True)
    IS_SPONSOR = db.Column(db.Integer, nullable=True)
    IS_GRANT = db.Column(db.Integer, nullable=True)
    IS_COMMITTEE_CONFLICT = db.Column(db.Integer, nullable=True)
    DSMB = db.Column(db.Integer, nullable=True)
    DSMB_FREQUENCY = db.Column(db.Integer, nullable=True)
    IS_DB = db.Column(db.Integer, nullable=True)
    IS_UVA_DB = db.Column(db.Integer, nullable=True)
    IS_CENTRAL_REG_DB = db.Column(db.Integer, nullable=True)
    IS_CONSENT_WAIVER = db.Column(db.Integer, nullable=True)
    IS_HGT = db.Column(db.Integer, nullable=True)
    IS_GENE_TRANSFER = db.Column(db.Integer, nullable=True)
    IS_TISSUE_BANKING = db.Column(db.Integer, nullable=True)
    IS_SURROGATE_CONSENT = db.Column(db.Integer, nullable=True)
    IS_ADULT_PARTICIPANT = db.Column(db.Integer, nullable=True)
    IS_MINOR_PARTICIPANT = db.Column(db.Integer, nullable=True)
    IS_MINOR = db.Column(db.Integer, nullable=True)
    IS_BIOMEDICAL = db.Column(db.Integer, nullable=True)
    IS_QUALITATIVE = db.Column(db.Integer, nullable=True)
    IS_PI_SCHOOL = db.Column(db.Integer, nullable=True)
    IS_PRISONERS_POP = db.Column(db.Integer, nullable=True)
    IS_PREGNANT_POP = db.Column(db.Integer, nullable=True)
    IS_FETUS_POP = db.Column(db.Integer, nullable=True)
    IS_MENTAL_IMPAIRMENT_POP = db.Column(db.Integer, nullable=True)
    IS_ELDERLY_POP = db.Column(db.Integer, nullable=True)
    IS_OTHER_VULNERABLE_POP = db.Column(db.Integer, nullable=True)
    OTHER_VULNERABLE_DESC = db.Column(db.String, nullable=True)
    IS_MULTI_SITE = db.Column(db.Integer, nullable=True)
    IS_UVA_LOCATION = db.Column(db.Integer, nullable=True)
    NON_UVA_LOCATION = db.Column(db.String, nullable=True)
    MULTI_SITE_LOCATIONS = db.Column(db.String, nullable=True)
    IS_OUTSIDE_CONTRACT = db.Column(db.Integer, nullable=True)
    IS_UVA_PI_MULTI = db.Column(db.Integer, nullable=True)
    IS_NOT_PRC_WAIVER = db.Column(db.Integer, nullable=True)
    IS_CANCER_PATIENT = db.Column(db.Integer, nullable=True)
    UPLOAD_COMPLETE = db.Column(db.Integer, nullable=True)
    IS_FUNDING_SOURCE = db.Column(db.Integer, nullable=True)
    IS_PI_INITIATED = db.Column(db.Integer, nullable=True)
    IS_ENGAGED_RESEARCH = db.Column(db.Integer, nullable=True)
    IS_APPROVED_DEVICE = db.Column(db.Integer, nullable=True)
    IS_FINANCIAL_CONFLICT = db.Column(db.Integer, nullable=True)
    IS_NOT_CONSENT_WAIVER = db.Column(db.Integer, nullable=True)
    IS_FOR_CANCER_CENTER = db.Column(db.Integer, nullable=True)
    IS_REVIEW_BY_CENTRAL_IRB = db.Column(db.Integer, nullable=True)
    IRBREVIEWERADMIN = db.Column(db.String, nullable=True)


class StudyDetailsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = StudyDetails
        load_instance = True
        include_relationships = False
