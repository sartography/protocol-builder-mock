from flask_table import Table, Col, DateCol, LinkCol, BoolCol, DatetimeCol, NestedTableCol
from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, SubmitField, StringField, IntegerField, BooleanField, DateField, widgets, \
    SelectField
from wtforms_alchemy import ModelForm

from models import RequiredDocument, Investigator, StudyDetails


class StudyForm(FlaskForm):
    TITLE = StringField('Title')
    NETBADGEID = StringField('UVA Id for Primary Investigator')
    requirements = SelectMultipleField("Requirements",
                                       render_kw={'class':'multi'},
                                       choices=[(rd.AUXDOCID, rd.AUXDOC) for rd in RequiredDocument.all()])
    HSRNUMBER = StringField('HSR Number')
    Q_COMPLETE = BooleanField('Complete in Protocol Builder?', default='checked',
                              false_values=(False, 'false', 0, '0'))

class InvestigatorForm(FlaskForm):
    NETBADGEID = StringField('UVA Id')
    INVESTIGATORTYPE = SelectField("InvestigatorType", choices=[(i.INVESTIGATORTYPE, i.INVESTIGATORTYPEFULL) for i in Investigator.all_types()])

class StudyDetailsForm(ModelForm, FlaskForm):
    class Meta:
        model = StudyDetails

class RequirementsTable(Table):
    AUXDOCID = Col('Code')
    AUXDOC = Col('Name')

class InvestigatorsTable(Table):
    NETBADGEID = Col('UVA Id')
    INVESTIGATORTYPE = Col('Type')
    delete = LinkCol('Delete', 'del_investigator', url_kwargs=dict(inv_id='id'))


class StudyTable(Table):
    def sort_url(self, col_id, reverse=False):
        pass
    edit = LinkCol('Edit', 'edit_study', url_kwargs=dict(study_id='STUDYID'))
    delete = LinkCol('Delete', 'del_study', url_kwargs=dict(study_id='STUDYID'))
    details = LinkCol('Details', 'study_details', url_kwargs=dict(study_id='STUDYID'))
    add_inv = LinkCol('Add Person', 'new_investigator', url_kwargs=dict(study_id='STUDYID'))
    STUDYID = Col('Study Id')
    TITLE = Col('Title')
    NETBADGEID = Col('User')
    DATE_MODIFIED = DatetimeCol('Last Update', "medium")
    Q_COMPLETE = BoolCol('Complete?')
    requirements = NestedTableCol('Requirements', RequirementsTable)
    investigators = NestedTableCol('Investigators', InvestigatorsTable)

