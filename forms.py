from flask_table import Table, Col, DateCol, LinkCol, BoolCol, DatetimeCol, NestedTableCol
from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, SubmitField, StringField, IntegerField, BooleanField, DateField, widgets, \
    SelectField

from models import RequiredDocument, Investigator


class StudySearchForm(FlaskForm):
    search = StringField('')


class StudyForm(FlaskForm):
    title = StringField('Title')
    netbadge_id = StringField('UVA Id for Primary Investigator')
    requirements = SelectMultipleField("Requirements",
                                       render_kw={'class':'multi'},
                                       choices=[(rd.code, rd.name) for rd in RequiredDocument.all()])
    hsr_number = StringField('HSR Number')
    q_complete = BooleanField('Complete in Protocol Builder?', default='checked',
                              false_values=(False, 'false', 0, '0'))
    # last_updated = DateField('Last Updated')

class InvestigatorForm(FlaskForm):
    netbadge_id = StringField('UVA Id')
    type = SelectField("InvestigatorType", choices=[(i.type, i.description) for i in Investigator.all_types()])

class RequirementsTable(Table):
    code = Col('Code')
    name = Col('Name')

class InvestigatorsTable(Table):
    netbadge_id = Col('UVA Id')
    type = Col('Type')
    delete = LinkCol('Delete', 'del_investigator', url_kwargs=dict(inv_id='id'))


class StudyTable(Table):
    def sort_url(self, col_id, reverse=False):
        pass
    edit = LinkCol('Edit', 'edit_study', url_kwargs=dict(study_id='study_id'))
    delete = LinkCol('Delete', 'del_study', url_kwargs=dict(study_id='study_id'))
    add_inv = LinkCol('Add Person', 'new_investigator', url_kwargs=dict(study_id='study_id'))
    study_id = Col('Study Id')
    title = Col('Title')
    netbadge_id = Col('User')
    last_updated = DatetimeCol('Last Update', "medium")
    q_complete = BoolCol('Complete?')
    requirements = NestedTableCol('Requirements', RequirementsTable)
    investigators = NestedTableCol('Investigators', InvestigatorsTable)

