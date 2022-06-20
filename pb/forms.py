from flask_table import Table, Col, LinkCol, BoolCol, DatetimeCol, NestedTableCol
from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, StringField, BooleanField, SelectField, validators, HiddenField, DateField, IntegerField
from wtforms.widgets import DateInput
from wtforms_alchemy import ModelForm
from wtforms.validators import Optional

from pb.models import RequiredDocument, Investigator, StudyDetails, IRBStatus, IRBInfo, IRBInfoEvent, IRBInfoStatus


class StudyForm(FlaskForm):
    STUDYID = HiddenField()
    TITLE = StringField('Title', [validators.DataRequired()])
    NETBADGEID = StringField('User UVA Computing Id', [validators.DataRequired()])
    requirements = SelectMultipleField("Documents",
                                       render_kw={'class': 'multi'},
                                       choices=[(rd.SS_AUXILIARY_DOC_TYPE_ID, rd.AUXILIARY_DOC) for rd in RequiredDocument.all()])
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
    IRB_REVIEW_TYPE = SelectField("IRB_REVIEW_TYPE",
                                  choices=['None', 'Full Committee', 'Expedited', 'Non-UVA IRB Full Board', 'Non-UVA IRB Expedited'])
    IRBEVENT = SelectField("IRBEVENT_ID / IRBEVENT",
                           choices=[((q.EVENT_ID, q.EVENT), f"{q.EVENT_ID} {q.EVENT}") for q in IRBInfoEvent.all()])
    IRB_STATUS = SelectField("IRB_STATUS_ID / IRB_STATUS",
                             choices=[((q.STATUS_ID, q.STATUS), f"{q.STATUS_ID} {q.STATUS}") for q in IRBInfoStatus.all()])
    IRB_OF_RECORD = StringField('IRB_OF_RECORD')
    UVA_IRB_HSR_IS_IRB_OF_RECORD_FOR_ALL_SITES = SelectField('UVA_IRB_HSR_IS_IRB_OF_RECORD_FOR_ALL_SITES',
                                                             choices=['None', '0', '1'],
                                                             coerce=irb_to_int)
    STUDYIRBREVIEWERADMIN = StringField('STUDYIRBREVIEWERADMIN')
    IRB_ONLINE_STATUS = SelectField("STATUS / DETAIL",
                                    choices=[('Downloaded', 'Downloaded / Study downloaded to IRB Online.'),
                                             ('Error', 'Error / Study not downloaded to IRB Online.')])


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
    IS_IND = IntegerField(validators=[Optional()], label='IS_IND')
    UVA_STUDY_TRACKING = StringField(label='UVA_STUDY_TRACKING')
    IND_1 = StringField(label='IND_1')
    IND_2 = StringField(label='IND_2')
    IND_3 = StringField(label='IND_3')
    IS_UVA_IND = IntegerField(validators=[Optional()], label='IS_UVA_IND')
    IS_IDE = IntegerField(validators=[Optional()], label='IS_IDE')
    IDE = StringField(label='IDE')
    IS_UVA_IDE = IntegerField(validators=[Optional()], label='IS_UVA_IDE')
    IS_CHART_REVIEW = IntegerField(validators=[Optional()], label='IS_CHART_REVIEW')
    IS_RADIATION = IntegerField(validators=[Optional()], label='IS_RADIATION')
    GCRC_NUMBER = StringField(label='GCRC_NUMBER')
    IS_GCRC = IntegerField(validators=[Optional()], label='IS_GCRC')
    IS_PRC_DSMP = IntegerField(validators=[Optional()], label='IS_PRC_DSMP')
    IS_PRC = IntegerField(validators=[Optional()], label='IS_PRC')
    PRC_NUMBER = StringField(label='PRC_NUMBER')
    IS_IBC = IntegerField(validators=[Optional()], label='IS_IBC')
    IBC_NUMBER = StringField(label='IBC_NUMBER')
    IS_SPONSOR_TRACKING = IntegerField(validators=[Optional()], label='IS_SPONSOR_TRACKING')
    SPONSOR_TRACKING = IntegerField(validators=[Optional()], label='SPONSOR_TRACKING')
    SPONSORS_PROTOCOL_REVISION_DATE = DateField(validators=[Optional()], label='SPONSORS_PROTOCOL_REVISION_DATE')
    IS_SPONSOR_MONITORING = IntegerField(validators=[Optional()], label='IS_SPONSOR_MONITORING')
    IS_DSMB = IntegerField(validators=[Optional()], label='IS_DSMB')
    IS_COMPLETE_NON_IRB_REGULATORY = IntegerField(validators=[Optional()], label='IS_COMPLETE_NON_IRB_REGULATORY')
    IS_AUX = IntegerField(validators=[Optional()], label='IS_AUX')
    IS_SPONSOR = IntegerField(validators=[Optional()], label='IS_SPONSOR')
    IS_GRANT = IntegerField(validators=[Optional()], label='IS_GRANT')
    IS_COMMITTEE_CONFLICT = IntegerField(validators=[Optional()], label='IS_COMMITTEE_CONFLICT')
    DSMB = StringField(label='DSMB')
    DSMB_FREQUENCY = IntegerField(validators=[Optional()], label='DSMB_FREQUENCY')
    IS_DB = IntegerField(validators=[Optional()], label='IS_DB')
    IS_UVA_DB = IntegerField(validators=[Optional()], label='IS_UVA_DB')
    IS_CENTRAL_REG_DB = IntegerField(validators=[Optional()], label='IS_CENTRAL_REG_DB')
    IS_CONSENT_WAIVER = IntegerField(validators=[Optional()], label='IS_CONSENT_WAIVER')
    IS_HGT = IntegerField(validators=[Optional()], label='IS_HGT')
    IS_GENE_TRANSFER = IntegerField(validators=[Optional()], label='IS_GENE_TRANSFER')
    IS_TISSUE_BANKING = IntegerField(validators=[Optional()], label='IS_TISSUE_BANKING')
    IS_SURROGATE_CONSENT = IntegerField(validators=[Optional()], label='IS_SURROGATE_CONSENT')
    IS_ADULT_PARTICIPANT = IntegerField(validators=[Optional()], label='IS_ADULT_PARTICIPANT')
    IS_MINOR_PARTICIPANT = IntegerField(validators=[Optional()], label='IS_MINOR_PARTICIPANT')
    IS_MINOR = IntegerField(validators=[Optional()], label='IS_MINOR')
    IS_BIOMEDICAL = IntegerField(validators=[Optional()], label='IS_BIOMEDICAL')
    IS_QUALITATIVE = IntegerField(validators=[Optional()], label='IS_QUALITATIVE')
    IS_PI_SCHOOL = IntegerField(validators=[Optional()], label='IS_PI_SCHOOL')
    IS_PRISONERS_POP = IntegerField(validators=[Optional()], label='IS_PRISONERS_POP')
    IS_PREGNANT_POP = IntegerField(validators=[Optional()], label='IS_PREGNANT_POP')
    IS_FETUS_POP = IntegerField(validators=[Optional()], label='IS_FETUS_POP')
    IS_MENTAL_IMPAIRMENT_POP = IntegerField(validators=[Optional()], label='IS_MENTAL_IMPAIRMENT_POP')
    IS_ELDERLY_POP = IntegerField(validators=[Optional()], label='IS_ELDERLY_POP')
    IS_OTHER_VULNERABLE_POP = IntegerField(validators=[Optional()], label='IS_OTHER_VULNERABLE_POP')
    OTHER_VULNERABLE_DESC = StringField(label='OTHER_VULNERABLE_DESC')
    IS_MULTI_SITE = IntegerField(validators=[Optional()], label='IS_MULTI_SITE')
    IS_UVA_LOCATION = IntegerField(validators=[Optional()], label='IS_UVA_LOCATION')
    NON_UVA_LOCATION = StringField(label='NON_UVA_LOCATION')
    MULTI_SITE_LOCATIONS = StringField(label='MULTI_SITE_LOCATIONS')
    IS_OUTSIDE_CONTRACT = IntegerField(validators=[Optional()], label='IS_OUTSIDE_CONTRACT')
    IS_UVA_PI_MULTI = IntegerField(validators=[Optional()], label='IS_UVA_PI_MULTI')
    IS_NOT_PRC_WAIVER = IntegerField(validators=[Optional()], label='IS_NOT_PRC_WAIVER')
    IS_INSIDE_CONTRACT = IntegerField(validators=[Optional()], label='IS_INSIDE_CONTRACT')
    IS_CANCER_PATIENT = IntegerField(validators=[Optional()], label='IS_CANCER_PATIENT')
    UPLOAD_COMPLETE = IntegerField(validators=[Optional()], label='UPLOAD_COMPLETE')
    IS_FUNDING_SOURCE = IntegerField(validators=[Optional()], label='IS_FUNDING_SOURCE')
    IS_CODED_RESEARCH = IntegerField(validators=[Optional()], label='IS_CODED_RESEARCH')
    IS_OUTSIDE_SPONSOR = IntegerField(validators=[Optional()], label='IS_OUTSIDE_SPONSOR')
    IS_PI_INITIATED = IntegerField(validators=[Optional()], label='IS_PI_INITIATED')
    IS_ENGAGED_RESEARCH = IntegerField(validators=[Optional()], label='IS_ENGAGED_RESEARCH')
    IS_APPROVED_DEVICE = IntegerField(validators=[Optional()], label='IS_APPROVED_DEVICE')
    IS_FINANCIAL_CONFLICT = IntegerField(validators=[Optional()], label='IS_FINANCIAL_CONFLICT')
    IS_NOT_CONSENT_WAIVER = IntegerField(validators=[Optional()], label='IS_NOT_CONSENT_WAIVER')
    IS_FOR_CANCER_CENTER = IntegerField(validators=[Optional()], label='IS_FOR_CANCER_CENTER')
    IS_REVIEW_BY_CENTRAL_IRB = IntegerField(validators=[Optional()], label='IS_REVIEW_BY_CENTRAL_IRB')
    IRBREVIEWERADMIN = StringField(label='IRBREVIEWERADMIN')
    IS_UVA_COLLABANALYSIS = IntegerField(validators=[Optional()], label='IS_UVA_COLLABANALYSIS')
    REVIEW_TYPE = SelectField("REVIEW_TYPE/REVIEWTYPENAME",
                              choices=[('1', ('1 None')),
                                       ('2', ('2 Full Committee')),
                                       ('3', ('3 Expedited')),
                                       ('21', ('21 Review by Non-UVA IRB'))])


class ConfirmDeleteForm(FlaskForm):
    confirm = BooleanField('Yes, really delete', default='checked',
                           false_values=(False, 'false', 0, '0'))


class RequirementsTable(Table):
    SS_AUXILIARY_DOC_TYPE_ID = Col('Code')
    AUXILIARY_DOC = Col('Name')


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

