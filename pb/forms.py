from flask_table import Table, Col, LinkCol, BoolCol, DatetimeCol, NestedTableCol
from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, StringField, BooleanField, SelectField, validators, HiddenField
from wtforms_alchemy import ModelForm

from pb.models import RequiredDocument, Investigator, StudyDetails


class StudyForm(FlaskForm):
    STUDYID = HiddenField()
    TITLE = StringField('Title', [validators.DataRequired()])
    NETBADGEID = StringField('User UVA Computing Id', [validators.DataRequired()])
    requirements = SelectMultipleField("Requirements",
                                       render_kw={'class': 'multi'},
                                       choices=[(rd.AUXDOCID, rd.AUXDOC) for rd in RequiredDocument.all()])
    HSRNUMBER = StringField('HSR Number')
    Q_COMPLETE = BooleanField('Complete in Protocol Builder?', default='checked',
                              false_values=(False, 'false', 0, '0'))


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
    STUDYID = Col('Study Id')
    TITLE = Col('Title')
    NETBADGEID = Col('User')
    DATE_MODIFIED = DatetimeCol('Last Update', "medium")
    Q_COMPLETE = BoolCol('Complete?')
    requirements = NestedTableCol('Requirements', RequirementsTable)
    investigators = NestedTableCol('Investigators', InvestigatorsTable)
    sponsors = NestedTableCol('Sponsors', SponsorsTable)
    delete = LinkCol(
        'delete', 'del_study', url_kwargs=dict(study_id='STUDYID'),
        anchor_attrs={'class': 'btn btn-icon btn-warn', 'title': 'Delete Study'},
        th_html_attrs={'class': 'mat-icon text-center', 'title': 'Delete Study'}
    )

