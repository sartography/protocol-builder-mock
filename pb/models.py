from marshmallow import fields
from sqlalchemy import func
from pb import db, ma
from marshmallow_sqlalchemy import SQLAlchemySchema
from sqlalchemy.orm import backref, dynamic


class Sponsor(db.Model):
    SPONSOR_ID = db.Column(db.Integer, primary_key=True)
    SP_NAME = db.Column(db.String, nullable=True)
    SP_MAILING_ADDRESS = db.Column(db.String, nullable=True)
    SP_PHONE = db.Column(db.String, nullable=True)
    SP_FAX = db.Column(db.String, nullable=True)
    SP_EMAIL = db.Column(db.String, nullable=True)
    SP_HOMEPAGE = db.Column(db.String, nullable=True)
    COMMONRULEAGENCY = db.Column(db.Boolean, nullable=True)
    SP_TYPE = db.Column(db.String, nullable=True)
    SP_TYPE_GROUP_NAME = db.Column(db.String, nullable=True)

    @staticmethod
    def all_types():
        types = [
            Sponsor(SP_TYPE="Federal", SP_TYPE_GROUP_NAME="Government"),
            Sponsor(SP_TYPE="Foundation/Not for Profit", SP_TYPE_GROUP_NAME="Other External Funding"),
            Sponsor(SP_TYPE="Incoming Sub Award", SP_TYPE_GROUP_NAME="Government"),
            Sponsor(SP_TYPE="Industry", SP_TYPE_GROUP_NAME="Industry"),
            Sponsor(SP_TYPE="Internal/Departmental/Gift", SP_TYPE_GROUP_NAME="Internal Funding"),
            Sponsor(SP_TYPE="No Funding", SP_TYPE_GROUP_NAME="Internal Funding"),
            Sponsor(SP_TYPE="Other Colleges and Universities", SP_TYPE_GROUP_NAME="Other External Funding"),
            Sponsor(SP_TYPE="State", SP_TYPE_GROUP_NAME="Government"),
        ]
        return types

    @staticmethod
    def get_type_group_name(type_code):
        for t in Sponsor.all_types():
            if t.SP_TYPE == type_code:
                return t.SP_TYPE_GROUP_NAME


class SponsorSchema(ma.Schema):
    class Meta:
        fields = ("SPONSOR_ID", "SP_NAME", "SP_MAILING_ADDRESS",
                  "SP_PHONE", "SP_FAX", "SP_EMAIL", "SP_HOMEPAGE",
                  "COMMONRULEAGENCY", "SP_TYPE")


class StudySponsor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    SS_STUDY = db.Column(db.Integer, db.ForeignKey('study.STUDYID'))
    SPONSOR_ID = db.Column(db.Integer, db.ForeignKey('sponsor.SPONSOR_ID'))
    study = db.relationship("Study", back_populates="sponsors")
    sponsor = db.relationship("Sponsor")


class StudySponsorSchema(ma.Schema):

    class Meta:
        fields = ("SS_STUDY", "SPONSOR_ID", "SP_NAME", "SP_TYPE", "SP_TYPE_GROUP_NAME", "COMMONRULEAGENCY")

    SP_TYPE = fields.Function(lambda obj: obj.sponsor.SP_TYPE)
    SP_NAME = fields.Function(lambda obj: obj.sponsor.SP_NAME)
    SP_TYPE_GROUP_NAME = fields.Function(lambda obj: obj.sponsor.SP_TYPE_GROUP_NAME)
    COMMONRULEAGENCY = fields.Function(lambda obj: obj.sponsor.COMMONRULEAGENCY)


class Study(db.Model):
    STUDYID = db.Column(db.Integer, primary_key=True)
    TITLE = db.Column(db.Text(), nullable=False)
    NETBADGEID = db.Column(db.String(), nullable=False)
    DATE_MODIFIED = db.Column(db.DateTime(timezone=True), default=func.now())
    Q_COMPLETE = db.relationship("IRBStatus", backref="study", lazy='dynamic')
    irb_info = db.relationship("IRBInfo", backref="study", lazy='dynamic')
    requirements = db.relationship("RequiredDocument", backref="study", lazy='dynamic')
    investigators = db.relationship("Investigator", backref="study", lazy='dynamic')
    study_details = db.relationship("StudyDetails", uselist=False, backref="study")
    sponsors = db.relationship("StudySponsor", back_populates="study", cascade="all, delete, delete-orphan")
    # This is a hack to get PB Mock up and running
    # We need to decide what to do about HSRNUMBER
    # TODO: Resolve HSRNUMBER issue
    HSRNUMBER = "0"


class IRBInfoEvent(db.Model):
    STUDY_ID = db.Column(db.Integer, db.ForeignKey('irb_info.SS_STUDY_ID'), primary_key=True)
    EVENT_ID = db.Column(db.String(), nullable=False, default='')
    EVENT = db.Column(db.String(), nullable=False, default='')

    @staticmethod
    def all():
        event = [IRBInfoEvent(EVENT_ID='', EVENT=''),
                 IRBInfoEvent(EVENT_ID='299', EVENT='PreReview Returned to PI New Protocol'),
                 IRBInfoEvent(EVENT_ID='2', EVENT='Pending Full Committee Review'),
                 IRBInfoEvent(EVENT_ID='57', EVENT='Approval New Protocol'),
                 IRBInfoEvent(EVENT_ID='300', EVENT='Approvable with Conditions-New Protocol'),
                 IRBInfoEvent(EVENT_ID='312', EVENT='Condition Response Accepted-New Protocol'),
                 IRBInfoEvent(EVENT_ID='316', EVENT='Deferred New Protocol'),
                 IRBInfoEvent(EVENT_ID='62', EVENT='Closed by PI')]
        return event


class IRBInfoEventSchema(SQLAlchemySchema):
    class Meta:
        model = IRBInfoEvent


class IRBInfoStatus(db.Model):
    STUDY_ID = db.Column(db.Integer, db.ForeignKey('irb_info.SS_STUDY_ID'), primary_key=True)
    STATUS_ID = db.Column(db.String(), nullable=False, default='')
    STATUS = db.Column(db.String(), nullable=False, default='')

    @staticmethod
    def all():
        status = [IRBInfoStatus(STATUS_ID='', STATUS=''),
                  IRBInfoStatus(STATUS_ID='30', STATUS='In PreReview New Protocol'),
                  IRBInfoStatus(STATUS_ID='31', STATUS='PreReview Complete New Protocol'),
                  IRBInfoStatus(STATUS_ID='2', STATUS='Open to enrollment'),
                  IRBInfoStatus(STATUS_ID='39', STATUS='Withdrawn'),
                  IRBInfoStatus(STATUS_ID='37', STATUS='Disapproved')]
        return status


class IRBInfoStatusSchema(SQLAlchemySchema):
    class Meta:
        model = IRBInfoStatus


class IRBInfo(db.Model):
    SS_STUDY_ID = db.Column(db.Integer, db.ForeignKey('study.STUDYID'), primary_key=True)
    UVA_STUDY_TRACKING = db.Column(db.String(), nullable=False, default='')
    DATE_MODIFIED = db.Column(db.Date, nullable=True)
    IRB_ADMINISTRATIVE_REVIEWER = db.Column(db.String(), nullable=False, default='')
    AGENDA_DATE = db.Column(db.Date, nullable=True)
    IRB_REVIEW_TYPE = db.Column(db.String(), nullable=False, default='')
    IRBEVENT = db.relationship("IRBInfoEvent", backref=backref("irb_info_event"), lazy='dynamic')
    IRB_STATUS = db.relationship("IRBInfoStatus", backref=backref("irb_info_status"), lazy='dynamic')
    IRB_OF_RECORD = db.Column(db.String(), nullable=False, default='')
    UVA_IRB_HSR_IS_IRB_OF_RECORD_FOR_ALL_SITES = db.Column(db.Integer(), nullable=True)
    STUDYIRBREVIEWERADMIN = db.Column(db.String(), nullable=False, default='')


class IRBInfoSchema(ma.Schema):
    class Meta:
        model = IRBInfo
        include_relationships = True
        load_instance = True
        fields = ("UVA_STUDY_TRACKING", "DATE_MODIFIED", "IRB_ADMINISTRATIVE_REVIEWER",
                  "AGENDA_DATE", "IRB_REVIEW_TYPE", "IRB_OF_RECORD", "IRBEVENT", "IRBEVENT_ID", "IRB_STATUS", "IRB_STATUS_ID",
                  "UVA_IRB_HSR_IS_IRB_OF_RECORD_FOR_ALL_SITES", "STUDYIRBREVIEWERADMIN")

    IRBEVENT = fields.Method("get_event")
    IRBEVENT_ID = fields.Method("get_event_id")
    IRB_STATUS = fields.Method("get_status")
    IRB_STATUS_ID = fields.Method("get_status_id")

    @staticmethod
    def get_event(obj):
        if obj is not None and hasattr(obj, 'IRBEVENT'):
            return obj.IRBEVENT[0].EVENT

    @staticmethod
    def get_event_id(obj):
        if obj is not None and hasattr(obj, 'IRBEVENT'):
            return obj.IRBEVENT[0].EVENT_ID

    @staticmethod
    def get_status(obj):
        if obj is not None and hasattr(obj, 'IRB_STATUS'):
            return obj.IRB_STATUS[0].STATUS

    @staticmethod
    def get_status_id(obj):
        if obj is not None and hasattr(obj, 'IRB_STATUS'):
            return obj.IRB_STATUS[0].STATUS_ID


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
        ]
        return types

    def set_type(self, type_code):
        self.INVESTIGATORTYPE = type_code
        for t in self.all_types():
            if t.INVESTIGATORTYPE == type_code:
                self.INVESTIGATORTYPEFULL = t.INVESTIGATORTYPEFULL


class InvestigatorSchema(ma.Schema):
    class Meta:
        fields = ("STUDYID", "NETBADGEID", "INVESTIGATORTYPE", "INVESTIGATORTYPEFULL")


class RequiredDocument(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    SS_AUXILIARY_DOC_TYPE_ID = db.Column(db.String(), nullable=False, default="")
    AUXILIARY_DOC = db.Column(db.String(), nullable=False, default="")
    STUDYID = db.Column(db.Integer, db.ForeignKey('study.STUDYID'))

    @staticmethod
    def all():
        docs = [RequiredDocument(SS_AUXILIARY_DOC_TYPE_ID=1, AUXILIARY_DOC="Investigators Brochure"),
                RequiredDocument(SS_AUXILIARY_DOC_TYPE_ID=2, AUXILIARY_DOC="Screening Log"),
                RequiredDocument(SS_AUXILIARY_DOC_TYPE_ID=3, AUXILIARY_DOC="Protocol"),
                RequiredDocument(SS_AUXILIARY_DOC_TYPE_ID=6, AUXILIARY_DOC="Cancer Center's PRC Approval Form"),
                RequiredDocument(SS_AUXILIARY_DOC_TYPE_ID=7, AUXILIARY_DOC="GCRC Approval Form"),
                RequiredDocument(SS_AUXILIARY_DOC_TYPE_ID=8, AUXILIARY_DOC="SOM CTO IND/IDE Review Letter"),
                RequiredDocument(SS_AUXILIARY_DOC_TYPE_ID=9, AUXILIARY_DOC="HIRE Approval"),
                RequiredDocument(SS_AUXILIARY_DOC_TYPE_ID=10, AUXILIARY_DOC="Cancer Center's PRC Approval Waiver"),
                RequiredDocument(SS_AUXILIARY_DOC_TYPE_ID=11, AUXILIARY_DOC="HSR Grant"),
                RequiredDocument(SS_AUXILIARY_DOC_TYPE_ID=12, AUXILIARY_DOC="Certificate of Confidentiality Application"),
                RequiredDocument(SS_AUXILIARY_DOC_TYPE_ID=14, AUXILIARY_DOC="Institutional Biosafety Committee Approval"),
                RequiredDocument(SS_AUXILIARY_DOC_TYPE_ID=18, AUXILIARY_DOC="SOM CTO Approval Letter - UVA PI Multisite Trial"),
                RequiredDocument(SS_AUXILIARY_DOC_TYPE_ID=19, AUXILIARY_DOC="IRB Approval or Letter of Approval from Administration: Send Data or Specimens to UVA"),
                RequiredDocument(SS_AUXILIARY_DOC_TYPE_ID=20, AUXILIARY_DOC="IRB Approval or Letter of Approval from Administration: Study Conducted at non- UVA Facilities "),
                RequiredDocument(SS_AUXILIARY_DOC_TYPE_ID=21, AUXILIARY_DOC="New Medical Device Form"),
                RequiredDocument(SS_AUXILIARY_DOC_TYPE_ID=22, AUXILIARY_DOC="SOM CTO Review regarding need for IDE"),
                RequiredDocument(SS_AUXILIARY_DOC_TYPE_ID=23, AUXILIARY_DOC="SOM CTO Review regarding need for IND"),
                RequiredDocument(SS_AUXILIARY_DOC_TYPE_ID=24, AUXILIARY_DOC="InfoSec Approval"),
                RequiredDocument(SS_AUXILIARY_DOC_TYPE_ID=25, AUXILIARY_DOC="Scientific Pre-review Documentation"),
                RequiredDocument(SS_AUXILIARY_DOC_TYPE_ID=26, AUXILIARY_DOC="IBC Number"),
                RequiredDocument(SS_AUXILIARY_DOC_TYPE_ID=32, AUXILIARY_DOC="IDS - Investigational Drug Service Approval"),
                RequiredDocument(SS_AUXILIARY_DOC_TYPE_ID=33, AUXILIARY_DOC="Data Security Plan"),
                RequiredDocument(SS_AUXILIARY_DOC_TYPE_ID=35, AUXILIARY_DOC="Model Consent"),
                RequiredDocument(SS_AUXILIARY_DOC_TYPE_ID=36, AUXILIARY_DOC="RDRC Approval "),
                RequiredDocument(SS_AUXILIARY_DOC_TYPE_ID=39, AUXILIARY_DOC="Age of Majority Cover Letter and Consent"),
                RequiredDocument(SS_AUXILIARY_DOC_TYPE_ID=40, AUXILIARY_DOC="SBS/IRB Approval-FERPA"),
                RequiredDocument(SS_AUXILIARY_DOC_TYPE_ID=41, AUXILIARY_DOC="HIRE Standard Radiation Language"),
                RequiredDocument(SS_AUXILIARY_DOC_TYPE_ID=42, AUXILIARY_DOC="COI Management Plan"),
                RequiredDocument(SS_AUXILIARY_DOC_TYPE_ID=43, AUXILIARY_DOC="SOM CTO Approval Letter-Non UVA, Non Industry PI MultiSite Study"),
                RequiredDocument(SS_AUXILIARY_DOC_TYPE_ID=44, AUXILIARY_DOC="GRIME Approval"),
                RequiredDocument(SS_AUXILIARY_DOC_TYPE_ID=45, AUXILIARY_DOC="GMEC Approval"),
                RequiredDocument(SS_AUXILIARY_DOC_TYPE_ID=46, AUXILIARY_DOC="IRB Reliance Agreement Request Form- IRB-HSR is IRB of Record"),
                RequiredDocument(SS_AUXILIARY_DOC_TYPE_ID=47, AUXILIARY_DOC="Non UVA IRB Approval - Initial and Last Continuation"),
                RequiredDocument(SS_AUXILIARY_DOC_TYPE_ID=48, AUXILIARY_DOC="MR Physicist Approval- Use of Gadolinium"),
                RequiredDocument(SS_AUXILIARY_DOC_TYPE_ID=49, AUXILIARY_DOC="SOM CTO Approval- Non- UVA Academia PI of IDE"),
                RequiredDocument(SS_AUXILIARY_DOC_TYPE_ID=51, AUXILIARY_DOC="IDS Waiver"),
                RequiredDocument(SS_AUXILIARY_DOC_TYPE_ID=52, AUXILIARY_DOC="Package Inserts"),
                RequiredDocument(SS_AUXILIARY_DOC_TYPE_ID=53, AUXILIARY_DOC="IRB Reliance Agreement Request Form- IRB-HSR Not IRB of Record"),
                RequiredDocument(SS_AUXILIARY_DOC_TYPE_ID=54, AUXILIARY_DOC="ESCRO Approval"),
                RequiredDocument(SS_AUXILIARY_DOC_TYPE_ID=56, AUXILIARY_DOC="Unaffiliated Investigator Agreement "),
                RequiredDocument(SS_AUXILIARY_DOC_TYPE_ID=57, AUXILIARY_DOC="Laser Safety Officer Approval"),
                RequiredDocument(SS_AUXILIARY_DOC_TYPE_ID=58, AUXILIARY_DOC="FDA Letter granting IND/IDE# or exemption")]
        return docs


class RequiredDocumentSchema(ma.Schema):
    class Meta:
        fields = ("SS_AUXILIARY_DOC_TYPE_ID", "AUXILIARY_DOC")


class IRBStatus(db.Model):
    STUDYID = db.Column(db.Integer, db.ForeignKey('study.STUDYID'), primary_key=True)
    STATUS = db.Column(db.String(), nullable=False, default="")
    DETAIL = db.Column(db.String(), nullable=False, default="")

    @staticmethod
    def all():
        status = [IRBStatus(STATUS="Error", DETAIL="Study ID does not exist."),
                  IRBStatus(STATUS="Error", DETAIL="General study errors. UVA Study Tracking Number is missing or not formatted correctly."),
                  IRBStatus(STATUS="No Error", DETAIL="Passed validation.")]
        return status


class IRBStatusSchema(ma.Schema):
    class Meta:
        fields = ("STATUS", "DETAIL")


class CreatorStudySchema(ma.Schema):
    class Meta:
        model = Study
        include_relationships = True
        load_instance = True
        fields = ["STUDYID", "TITLE", "DATECREATED", "DATELASTMODIFIED", "REVIEW_TYPE"]
    DATECREATED = DATELASTMODIFIED = fields.Method("get_dates")
    REVIEW_TYPE = fields.Method("get_review_type")

    @staticmethod
    def get_dates(obj):
        if obj is not None and hasattr(obj, "DATE_MODIFIED"):
            return obj.DATE_MODIFIED

    @staticmethod
    def get_review_type(obj):
        if obj is not None and hasattr(obj, "study_details"):
            return obj.study_details.REVIEW_TYPE


class StudySchema(ma.Schema):
    class Meta:
        include_relationships = True
        load_instance = True
        # Fields to expose
        fields = ("STUDYID", "TITLE", "NETBADGEID",
                  "DATE_MODIFIED", "Q_COMPLETE", "HSRNUMBER")
    Q_COMPLETE = fields.Method("get_q_complete")
    # TODO: Resolve HSRNUMBER issue
    # Currently, we set HSRNUMBER to 0 in the model

    @staticmethod
    def get_q_complete(obj):
        """Ultimately, this will be calculated based on the contents of Q_COMPLETE.
        For now, we return the contents of Q_COMPLETE"""
        # TODO: Calculate whatever we need to calculate.
        # TODO: Currently, we don't return HSRNUMBER,
        #  but we don't currently use it in CR Connect either
        if obj is not None and hasattr(obj, 'Q_COMPLETE'):
            if len(obj.Q_COMPLETE.all()) > 0:
                return {'STATUS': obj.Q_COMPLETE[0].STATUS, 'DETAIL': obj.Q_COMPLETE[0].DETAIL}
        return {}


class StudyDetails(db.Model):
    STUDYID = db.Column(db.Integer, db.ForeignKey('study.STUDYID'), primary_key=True)
    UVA_STUDY_TRACKING = db.Column(db.String, nullable=True)
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
    SPONSORS_PROTOCOL_REVISION_DATE = db.Column(db.Date, nullable=True)
    IS_SPONSOR_MONITORING = db.Column(db.Integer, nullable=True)
    IS_AUX  = db.Column(db.Integer, nullable=True)
    IS_SPONSOR = db.Column(db.Integer, nullable=True)
    IS_GRANT = db.Column(db.Integer, nullable=True)
    IS_COMMITTEE_CONFLICT = db.Column(db.Integer, nullable=True)
    DSMB = db.Column(db.String, nullable=True)
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
    IS_SPONSOR_TRACKING = db.Column(db.Integer, nullable=True)
    SPONSOR_TRACKING = db.Column(db.Integer, nullable=True)
    IS_DSMB = db.Column(db.Integer, nullable=True)
    IS_COMPLETE_NON_IRB_REGULATORY = db.Column(db.Integer, nullable=True)
    IS_INSIDE_CONTRACT = db.Column(db.Integer, nullable=True)
    IS_CODED_RESEARCH = db.Column(db.Integer, nullable=True)
    IS_OUTSIDE_SPONSOR = db.Column(db.Integer, nullable=True)
    IS_UVA_COLLABANALYSIS = db.Column(db.Integer, nullable=True)
    REVIEW_TYPE = db.Column(db.Integer, nullable=True)
    REVIEWTYPENAME = db.Column(db.String, nullable=True)


class StudyDetailsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = StudyDetails
        load_instance = True
        include_relationships = False


class SelectedUser(db.Model):
    user_id = db.Column(db.String(), primary_key=True)
    selected_user = db.Column(db.String(), nullable=True)


class SelectedUserSchema(ma.Schema):
    class Meta:
        fields = ("user_id", "selected_user")

