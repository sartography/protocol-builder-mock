from flask_table import Table, Col, DateCol, LinkCol, BoolCol, DatetimeCol, NestedTableCol
from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, SubmitField, StringField, IntegerField, BooleanField, DateField, widgets

from models import RequiredDocument


class StudySearchForm(FlaskForm):
    search = StringField('')


class StudyForm(FlaskForm):
    title = StringField('Title')
    netbadge_id = StringField('UVA Id for Primary Investigator')
    requirements = SelectMultipleField("Requirements", choices=[(rd.code, rd.name) for rd in RequiredDocument.all()])
    hsr_number = StringField('HSR Number')
    q_complete = BooleanField('Complete in Protocol Builder?')
    # last_updated = DateField('Last Updated')


class RequirementsTable(Table):
    code = Col('Code')
    name = Col('Name')

class StudyTable(Table):
    def sort_url(self, col_id, reverse=False):
        pass
    edit = LinkCol('Edit', 'edit_study', url_kwargs=dict(study_id='study_id'))
    study_id = Col('Study Id')
    title = Col('Title')
    netbadge_id = Col('Primary Investigator')
    last_updated = DatetimeCol('Last Update', "medium")
    q_complete = BoolCol('Complete?')
    requirements = NestedTableCol('Requirements', RequirementsTable)

