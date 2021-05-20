from flask_table import Table, Col, LinkCol, BoolCol, DatetimeCol, NestedTableCol
from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, StringField, BooleanField, SelectField, validators, HiddenField, DateField, IntegerField
from wtforms_alchemy import ModelForm

from pb.models import RequiredDocument, RequiredDocumentsList, Investigator, StudyDetails, IRBStatus, IRBInfo


def get_study_form_choices():
    form_choices = RequiredDocumentsList().all()
    # form_choices = RequiredDocument().all()
    return form_choices

    # choices = [(rd.AUXDOCID, rd.AUXDOC) for rd in required_documents]
    # return choices

from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
class StudyForm(FlaskForm):
    STUDYID = HiddenField()
    TITLE = StringField('Title', [validators.DataRequired()])
    NETBADGEID = StringField('User UVA Computing Id', [validators.DataRequired()])
    requirements = QuerySelectMultipleField("Documents",
                                            render_kw={'class': 'multi'},
                                            query_factory=get_study_form_choices,
                                            get_label='AUXDOC')
    HSRNUMBER = StringField('HSR Number')
    Q_COMPLETE = SelectField("IRBStatus",
                             choices=[((q.STATUS, q.DETAIL), q.DETAIL) for q in IRBStatus.all()])


class IRBInfoForm(ModelForm, FlaskForm):
    class Meta:
        model = IRBInfo
        hidden = 'SS_STUDY_ID'


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


class StudyDetailsForm(ModelForm, FlaskForm):
    class Meta:
        model = StudyDetails
        only = ['IS_IND', 'IND_1', 'IND_2', 'IND_3', 'IS_UVA_IND', 'IS_IDE', 'IDE',
                'IS_UVA_IDE', 'IS_CHART_REVIEW', 'IS_RADIATION', 'GCRC_NUMBER', 'IS_GCRC',
                'IS_PRC_DSMP', 'IS_PRC', 'PRC_NUMBER', 'IS_IBC', 'IBC_NUMBER',
                'IS_SPONSOR_TRACKING', 'SPONSOR_TRACKING', 'SPONSORS_PROTOCOL_REVISION_DATE',
                'IS_SPONSOR_MONITORING', 'IS_DSMB', 'IS_COMPLETE_NON_IRB_REGULATORY',
                'IS_AUX', 'IS_SPONSOR', 'IS_GRANT', 'IS_COMMITTEE_CONFLICT', 'DSMB',
                'DSMB_FREQUENCY', 'IS_DB', 'IS_UVA_DB', 'IS_CENTRAL_REG_DB',
                'IS_CONSENT_WAIVER', 'IS_HGT', 'IS_GENE_TRANSFER', 'IS_TISSUE_BANKING',
                'IS_SURROGATE_CONSENT', 'IS_ADULT_PARTICIPANT', 'IS_MINOR_PARTICIPANT',
                'IS_MINOR', 'IS_BIOMEDICAL', 'IS_QUALITATIVE', 'IS_PI_SCHOOL',
                'IS_PRISONERS_POP', 'IS_PREGNANT_POP', 'IS_FETUS_POP',
                'IS_MENTAL_IMPAIRMENT_POP', 'IS_ELDERLY_POP', 'IS_OTHER_VULNERABLE_POP',
                'OTHER_VULNERABLE_DESC', 'IS_MULTI_SITE', 'IS_UVA_LOCATION',
                'NON_UVA_LOCATION', 'MULTI_SITE_LOCATIONS', 'IS_OUTSIDE_CONTRACT',
                'IS_UVA_PI_MULTI', 'IS_NOT_PRC_WAIVER', 'IS_INSIDE_CONTRACT',
                'IS_CANCER_PATIENT', 'UPLOAD_COMPLETE', 'IS_FUNDING_SOURCE',
                'IS_CODED_RESEARCH', 'IS_OUTSIDE_SPONSOR', 'IS_PI_INITIATED',
                'IS_ENGAGED_RESEARCH', 'IS_APPROVED_DEVICE', 'IS_FINANCIAL_CONFLICT',
                'IS_NOT_CONSENT_WAIVER', 'IS_FOR_CANCER_CENTER', 'IS_REVIEW_BY_CENTRAL_IRB',
                'IRBREVIEWERADMIN', 'IS_UVA_COLLABANALYSIS', 'REVIEW_TYPE', 'REVIEWTYPENAME']


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

