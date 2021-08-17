from flask_table import Table, Col, LinkCol, BoolCol, DatetimeCol, NestedTableCol
from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, StringField, BooleanField, SelectField, validators, HiddenField, DateField, IntegerField
from wtforms_alchemy import ModelForm
from wtforms.widgets.html5 import DateInput
from wtforms.validators import Optional

from pb.models import RequiredDocument, Investigator, StudyDetails, IRBStatus, IRBInfo, IRBInfoEvent, IRBInfoStatus


class StudyForm(FlaskForm):
    STUDYID = HiddenField()
    TITLE = StringField('Title', [validators.DataRequired()])
    NETBADGEID = StringField('User UVA Computing Id', [validators.DataRequired()])
    requirements = SelectMultipleField("Documents",
                                       render_kw={'class': 'multi'},
                                       choices=[(rd.AUXDOCID, rd.AUXDOC) for rd in RequiredDocument.all()])
    Q_COMPLETE = SelectField("IRBStatus",
                             choices=[((q.STATUS, q.DETAIL), q.DETAIL) for q in IRBStatus.all()])


def irb_to_int(x):
    if x == 'None':
        return None
    elif x == '0':
        return 0
    elif x == '1':
        return 1


class IRBInfoForm(FlaskForm):
    SS_STUDY_ID = HiddenField()
    UVA_STUDY_TRACKING = StringField('UVA_STUDY_TRACKING')
    DATE_MODIFIED = DateField('DATE_MODIFIED', [Optional()], widget=DateInput())
    IRB_ADMINISTRATIVE_REVIEWER = StringField('IRB_ADMINISTRATIVE_REVIEWER')
    AGENDA_DATE = DateField('AGENDA_DATE', [Optional()], widget=DateInput())
    IRB_REVIEW_TYPE = StringField('IRB_REVIEW_TYPE')
    IRBEVENT = SelectField("IRBInfoEvent",
                           choices=[((q.EVENT_ID, q.EVENT), q.EVENT) for q in IRBInfoEvent.all()])
    IRB_STATUS = SelectField("IRBInfoStatus",
                             choices=[((q.STATUS_ID, q.STATUS), q.STATUS) for q in IRBInfoStatus.all()])
    IRB_OF_RECORD = StringField('IRB_OF_RECORD')
    UVA_IRB_HSR_IS_IRB_OF_RECORD_FOR_ALL_SITES = SelectField('UVA_IRB_HSR_IS_IRB_OF_RECORD_FOR_ALL_SITES',
                                                             choices=['None', '0', '1'],
                                                             coerce=irb_to_int)
    STUDYIRBREVIEWERADMIN = StringField('STUDYIRBREVIEWERADMIN')


class InvestigatorForm(FlaskForm):
    NETBADGEID = StringField('UVA Id')
    INVESTIGATORTYPE = SelectField("InvestigatorType", choices=[(i.INVESTIGATORTYPE, i.INVESTIGATORTYPEFULL) for i in Investigator.all_types()])


class StudySponsorForm(FlaskForm):
    STUDY_ID = HiddenField()
    SPONSOR_IDS = SelectMultipleField(
        "Sponsor",
        coerce=int,
        render_kw={'class': 'multi'},
        validators=[validators.DataRequired()]
    )


class StudyDetailsForm(FlaskForm):
    STUDYID = HiddenField()
    IS_IND = IntegerField(validators=[Optional()])
    UVA_STUDY_TRACKING = StringField()
    IND_1 = StringField()
    IND_2 = StringField()
    IND_3 = StringField()
    IS_UVA_IND = IntegerField(validators=[Optional()])
    IS_IDE = IntegerField(validators=[Optional()])
    IDE = StringField()
    IS_UVA_IDE = IntegerField(validators=[Optional()])
    IS_CHART_REVIEW = IntegerField(validators=[Optional()])
    IS_RADIATION = IntegerField(validators=[Optional()])
    GCRC_NUMBER = StringField()
    IS_GCRC = IntegerField(validators=[Optional()])
    IS_PRC_DSMP = IntegerField(validators=[Optional()])
    IS_PRC = IntegerField(validators=[Optional()])
    PRC_NUMBER = StringField()
    IS_IBC = IntegerField(validators=[Optional()])
    IBC_NUMBER = StringField()
    IS_SPONSOR_TRACKING = IntegerField(validators=[Optional()])
    SPONSOR_TRACKING = IntegerField(validators=[Optional()])
    SPONSORS_PROTOCOL_REVISION_DATE = DateField(validators=[Optional()])
    IS_SPONSOR_MONITORING = IntegerField(validators=[Optional()])
    IS_DSMB = IntegerField(validators=[Optional()])
    IS_COMPLETE_NON_IRB_REGULATORY = IntegerField(validators=[Optional()])
    IS_AUX = IntegerField(validators=[Optional()])
    IS_SPONSOR = IntegerField(validators=[Optional()])
    IS_GRANT = IntegerField(validators=[Optional()])
    IS_COMMITTEE_CONFLICT = IntegerField(validators=[Optional()])
    DSMB = StringField()
    DSMB_FREQUENCY = IntegerField(validators=[Optional()])
    IS_DB = IntegerField(validators=[Optional()])
    IS_UVA_DB = IntegerField(validators=[Optional()])
    IS_CENTRAL_REG_DB = IntegerField(validators=[Optional()])
    IS_CONSENT_WAIVER = IntegerField(validators=[Optional()])
    IS_HGT = IntegerField(validators=[Optional()])
    IS_GENE_TRANSFER = IntegerField(validators=[Optional()])
    IS_TISSUE_BANKING = IntegerField(validators=[Optional()])
    IS_SURROGATE_CONSENT = IntegerField(validators=[Optional()])
    IS_ADULT_PARTICIPANT = IntegerField(validators=[Optional()])
    IS_MINOR_PARTICIPANT = IntegerField(validators=[Optional()])
    IS_MINOR = IntegerField(validators=[Optional()])
    IS_BIOMEDICAL = IntegerField(validators=[Optional()])
    IS_QUALITATIVE = IntegerField(validators=[Optional()])
    IS_PI_SCHOOL = IntegerField(validators=[Optional()])
    IS_PRISONERS_POP = IntegerField(validators=[Optional()])
    IS_PREGNANT_POP = IntegerField(validators=[Optional()])
    IS_FETUS_POP = IntegerField(validators=[Optional()])
    IS_MENTAL_IMPAIRMENT_POP = IntegerField(validators=[Optional()])
    IS_ELDERLY_POP = IntegerField(validators=[Optional()])
    IS_OTHER_VULNERABLE_POP = IntegerField(validators=[Optional()])
    OTHER_VULNERABLE_DESC = StringField()
    IS_MULTI_SITE = IntegerField(validators=[Optional()])
    IS_UVA_LOCATION = IntegerField(validators=[Optional()])
    NON_UVA_LOCATION = StringField()
    MULTI_SITE_LOCATIONS = StringField()
    IS_OUTSIDE_CONTRACT = IntegerField(validators=[Optional()])
    IS_UVA_PI_MULTI = IntegerField(validators=[Optional()])
    IS_NOT_PRC_WAIVER = IntegerField(validators=[Optional()])
    IS_INSIDE_CONTRACT = IntegerField(validators=[Optional()])
    IS_CANCER_PATIENT = IntegerField(validators=[Optional()])
    UPLOAD_COMPLETE = IntegerField(validators=[Optional()])
    IS_FUNDING_SOURCE = IntegerField(validators=[Optional()])
    IS_CODED_RESEARCH = IntegerField(validators=[Optional()])
    IS_OUTSIDE_SPONSOR = IntegerField(validators=[Optional()])
    IS_PI_INITIATED = IntegerField(validators=[Optional()])
    IS_ENGAGED_RESEARCH = IntegerField(validators=[Optional()])
    IS_APPROVED_DEVICE = IntegerField(validators=[Optional()])
    IS_FINANCIAL_CONFLICT = IntegerField(validators=[Optional()])
    IS_NOT_CONSENT_WAIVER = IntegerField(validators=[Optional()])
    IS_FOR_CANCER_CENTER = IntegerField(validators=[Optional()])
    IS_REVIEW_BY_CENTRAL_IRB = IntegerField(validators=[Optional()])
    IRBREVIEWERADMIN = StringField()
    IS_UVA_COLLABANALYSIS = IntegerField(validators=[Optional()])
    REVIEW_TYPE = SelectField("Review Type",
                              choices=[('1', ('1 None')),
                                       ('2', ('2 Full Committee')),
                                       ('3', ('3 Expedited')),
                                       ('23', ('23 Non-UVA IRB Full Board')),
                                       ('24', ('24 Non-UVA IRB Expedited'))])


class ConfirmDeleteForm(FlaskForm):
    confirm = BooleanField('Yes, really delete', default='checked',
                           false_values=(False, 'false', 0, '0'))


class RequirementsTable(Table):
    AUXDOCID = Col('Code')
    AUXDOC = Col('Name')


class InvestigatorsTable(Table):
    NETBADGEID = Col('UVA Id')
    INVESTIGATORTYPE = Col('Type')
    delete = LinkCol(
        'delete', 'del_investigator', url_kwargs=dict(inv_id='id'),
        anchor_attrs={'class': 'btn btn-icon btn-warn', 'title': 'Delete Investigator'},
        th_html_attrs={'class': 'mat-icon text-center', 'title': 'Delete Investigator'}
    )


class SponsorCol(Col):
    def td_format(self, content):
        return f'{content.SP_NAME} ({content.SP_TYPE})'


class SponsorsTable(Table):
    sponsor = SponsorCol('Sponsor')
    delete = LinkCol(
        'delete', 'del_study_sponsor', url_kwargs=dict(study_sponsor_id='id'),
        anchor_attrs={'class': 'btn btn-icon btn-warn', 'title': 'Delete Sponsor'},
        th_html_attrs={'class': 'mat-icon text-center', 'title': 'Delete Sponsor'}
    )


class StudyTable(Table):
    def sort_url(self, col_id, reverse=False):
        pass
    edit = LinkCol(
        'edit', 'edit_study', url_kwargs=dict(study_id='STUDYID'),
        anchor_attrs={'class': 'btn btn-icon btn-primary', 'title': 'Edit Study'},
        th_html_attrs={'class': 'mat-icon text-center', 'title': 'Edit Study'}
    )
    details = LinkCol(
        'ballot', 'study_details', url_kwargs=dict(study_id='STUDYID'),
        anchor_attrs={'class': 'btn btn-icon btn-default', 'title': 'Edit Questions'},
        th_html_attrs={'class': 'mat-icon text-center', 'title': 'Edit Questions'}
    )
    add_inv = LinkCol(
        'person_add', 'new_investigator', url_kwargs=dict(study_id='STUDYID'),
        anchor_attrs={'class': 'btn btn-icon btn-accent', 'title': 'Add Investigator'},
        th_html_attrs={'class': 'mat-icon text-center', 'title': 'Add Investigator'}
    )
    add_sponsor = LinkCol(
        'account_balance', 'edit_study_sponsor', url_kwargs=dict(study_id='STUDYID'),
        anchor_attrs={'class': 'btn btn-icon btn-accent', 'title': 'Edit Sponsor(s)'},
        th_html_attrs={'class': 'mat-icon text-center', 'title': 'Edit Sponsor(s)'}
    )
    irb_info = LinkCol(
        'info', 'edit_irb_info', url_kwargs=dict(study_id='STUDYID'),
        anchor_attrs={'class': 'btn btn-icon btn-accent', 'title': 'Edit Info'},
        th_html_attrs={'class': 'mat-icon text-center', 'title': 'Edit Info'}
    )
    STUDYID = Col('Study Id')
    TITLE = Col('Title')
    NETBADGEID = Col('User')
    DATE_MODIFIED = DatetimeCol('Last Update', "medium")
    Q_COMPLETE = BoolCol('Complete?')
    requirements = NestedTableCol('Documents', RequirementsTable)
    investigators = NestedTableCol('Investigators', InvestigatorsTable)
    sponsors = NestedTableCol('Sponsors', SponsorsTable)
    delete = LinkCol(
        'delete', 'del_study', url_kwargs=dict(study_id='STUDYID'),
        anchor_attrs={'class': 'btn btn-icon btn-warn', 'title': 'Delete Study'},
        th_html_attrs={'class': 'mat-icon text-center', 'title': 'Delete Study'}
    )

