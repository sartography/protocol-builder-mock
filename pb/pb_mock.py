from pb.models import Study, RequiredDocument, StudyDetails, IRBStatus, IRBInfo, SelectedUser
from pb.forms import StudyTable

from pb import BASE_HREF, app, db, session
from flask import g, render_template, redirect, url_for
from sqlalchemy import func
import datetime
import csv
from io import TextIOWrapper


def _is_production():
    return 'PRODUCTION' in app.config and app.config['PRODUCTION']


def _get_request_uid(req):
    uid = None
    if _is_production():
        if 'user' in g and g.user is not None:
            return g.user.uid
        uid = req.headers.get("Uid")
        if not uid:
            uid = req.headers.get("X-Remote-Uid")
    else:
        uid = 'current_user'

    return uid


def get_current_user(request):
    current_user = _get_request_uid(request)
    return current_user


def get_selected_user(current_user):
    result = db.session.query(SelectedUser).filter(SelectedUser.user_id == current_user).first()
    if result:
        selected_user = result.selected_user
        return selected_user


def update_selected_user(user, selected_user):
    model = SelectedUser(user_id=user, selected_user=selected_user)
    db_selected_user = db.session.query(SelectedUser).filter(SelectedUser.user_id==user).first()
    if db_selected_user:
        db_selected_user.selected_user = selected_user
    else:
        db_selected_user = model
        db.session.add(db_selected_user)
    db.session.commit()
    return db_selected_user


def render_study_template(studies, uva_id):
    table = StudyTable(studies)
    users = []
    [users.append(study.NETBADGEID) for study in db.session.query(Study).all() if study.NETBADGEID not in users]
    return render_template(
        'index.html',
        table=table,
        base_href=BASE_HREF,
        users=users,
        selected_user=uva_id
    )

def _update_study(study, form):
    if study.STUDYID is None:
        # quick hack to get auto-increment without creating a bunch of hassle, this is not
        # production code by any stretch of the imagination, but this is a throw away library.
        max_id = db.session.query(func.max(Study.STUDYID)).scalar() or 1

        study.STUDYID = max_id + 1
    else:
        # Delete existing required documents for this study.
        db.session.query(RequiredDocument).filter(RequiredDocument.STUDYID == study.STUDYID).delete()

    study.TITLE = form.TITLE.data
    study.NETBADGEID = form.NETBADGEID.data
    study.DATE_MODIFIED = datetime.datetime.now()
    study.HSRNUMBER = form.HSRNUMBER.data

    for r in form.requirements:
        if r.checked:
            requirement = RequiredDocument(AUXDOCID=r.data, AUXDOC=r.label.text, study=study)
            db.session.add(requirement)

    q_data = eval(form.Q_COMPLETE.data)
    if q_data:
        q_data_status = q_data[0]
        q_data_detail = q_data[1]
        q_status = db.session.query(IRBStatus).filter(IRBStatus.STUDYID == study.STUDYID).first()
        if q_status:
            q_status.STATUS = q_data_status
            q_status.DETAIL = q_data_detail
        else:
            q_status = IRBStatus(STATUS=q_data_status, DETAIL=q_data_detail, STUDYID=study.STUDYID)
        db.session.add(q_status)

    db.session.add(study)
    db.session.commit()


def _update_irb_info(study_id, irb_info, form):
    if irb_info is None:
        irb_info = IRBInfo(SS_STUDY_ID=study_id)
    irb_info.UVA_STUDY_TRACKING = form.UVA_STUDY_TRACKING.data
    irb_info.DATE_MODIFIED = form.DATE_MODIFIED.data
    irb_info.IRB_ADMINISTRATIVE_REVIEWER = form.IRB_ADMINISTRATIVE_REVIEWER.data
    irb_info.AGENDA_DATE = form.AGENDA_DATE.data
    irb_info.IRB_REVIEW_TYPE = form.IRB_REVIEW_TYPE.data
    irb_info.IRBEVENT = form.IRBEVENT.data
    irb_info.IRB_STATUS = form.IRB_STATUS.data
    irb_info.IRB_OF_RECORD = form.IRB_OF_RECORD.data
    irb_info.UVA_IRB_HSR_IS_IRB_OF_RECORD_FOR_ALL_SITES = form.UVA_IRB_HSR_IS_IRB_OF_RECORD_FOR_ALL_SITES.data
    irb_info.STUDYIRBREVIEWERADMIN = form.STUDYIRBREVIEWERADMIN.data

    db.session.add(irb_info)
    db.session.commit()


def _allowed_file(filename):
    allowed_extensions = ['csv', 'xls', 'xlsx']
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


def process_csv_study_details(study_id, csv_file):
    study_details = db.session.query(StudyDetails).filter(StudyDetails.STUDYID == study_id).first()
    csv_file.seek(0)
    data = csv.DictReader(TextIOWrapper(csv_file))
    for row in data:
        if data.line_num == 2:

            for key in row.keys():
                if key != 'STUDYID':
                    if hasattr(study_details, key):
                        if key in row.keys():
                            val = row[key]
                            print(key, val)
                            if key == 'SPONSORS_PROTOCOL_REVISION_DATE':
                                print(type(val))
                            if val == '':
                                val = None
                            if val == 'null':
                                val = None
                            setattr(study_details, key, val)

    session.add(study_details)
    session.commit()


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


def redirect_home():
    return redirect(url_for('index'))
