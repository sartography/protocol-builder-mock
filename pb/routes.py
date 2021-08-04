from flask import flash, redirect, render_template, request, url_for
from pb import app, db, description_map, session
from pb.ldap.ldap_service import LdapService
from pb.pb_mock import get_current_user, get_selected_user, update_selected_user, \
    render_study_template, _update_study, redirect_home, _update_irb_info, _allowed_file, \
    process_csv_study_details, has_no_empty_params, verify_required_document_list, verify_study_details_list
from pb.forms import StudyForm, IRBInfoForm, InvestigatorForm, ConfirmDeleteForm, StudySponsorForm, StudyDetailsForm
from pb.models import Study, StudyDetails, IRBInfo, IRBInfoEvent, IRBInfoStatus, IRBStatus, Investigator, Sponsor, StudySponsor, RequiredDocument

import json

BASE_HREF = app.config['APPLICATION_ROOT'].strip('/')


@app.route('/', methods=['GET', 'POST'])
def index():
    # If they have a selected_user,
    # redirect to /user_studies/{selected_user}
    # Otherwise, redirect to /user_studies/all
    redirect_url = url_for("user_studies", uva_id="all")
    current_user = get_current_user(request)
    if current_user:
        selected_user = get_selected_user(current_user)
        if selected_user:
            redirect_url = url_for("user_studies", uva_id=selected_user)
    return redirect(redirect_url)


@app.route('/user_studies/', defaults={'uva_id': 'all'})
@app.route('/user_studies/<uva_id>', methods=['GET'])
def user_studies(uva_id):
    if uva_id == 'all':
        # return redirect(BASE_HREF + "/")
        studies = db.session.query(Study).order_by(Study.DATE_MODIFIED.desc()).all()
    else:
        studies = db.session.query(Study).filter(Study.NETBADGEID == uva_id).order_by(Study.DATE_MODIFIED.desc()).all()
    current_user = get_current_user(request)
    update_selected_user(current_user, uva_id)
    return render_study_template(studies, uva_id)


# Used by frontend in e2e tests
# You can add valid=true to the url
# to set REVIEW_TYPE and REVIEWTYPENAME
@app.route('/new_test_study', methods=['POST'])
def new_test_study():
    form = StudyForm(request.form)
    study = Study()
    study.study_details = StudyDetails()
    if 'valid' in request.args and request.args['valid'] == 'true':
        study.study_details.REVIEW_TYPE = 2
        study.study_details.REVIEWTYPENAME = 'Full Committee'
    _update_study(study, form)
    print('new_test_study')


@app.route('/new_study', methods=['GET', 'POST'])
def new_study():
    form = StudyForm(request.form)
    action = BASE_HREF + "/new_study"
    title = "New Study"
    if request.method == 'POST':
        study = Study()
        study.study_details = StudyDetails()
        _update_study(study, form)
        flash('Study created successfully!', 'success')
        return redirect_home()

    # set default first time
    form.Q_COMPLETE.data = "('No Error', 'Passed validation.')"
    return render_template(
        'form.html',
        form=form,
        action=action,
        title=title,
        description_map=description_map,
        base_href=BASE_HREF
    )


@app.route('/study/<study_id>', methods=['GET', 'POST'])
def edit_study(study_id):
    study = db.session.query(Study).filter(Study.STUDYID == study_id).first()
    form = StudyForm(request.form, obj=study)
    if request.method == 'GET':
        if study.requirements:
            form.requirements.data = list(map(lambda r: r.AUXDOCID, list(study.requirements)))
        if study.Q_COMPLETE and study.Q_COMPLETE.first():
            form.Q_COMPLETE.data = "('" + study.Q_COMPLETE.first().STATUS + "', '" + study.Q_COMPLETE.first().DETAIL + "')"
        else:
            form.Q_COMPLETE.data = "('No Error', 'Passed validation.')"
    if request.method == 'POST':
        _update_study(study, form)
        flash('Study updated successfully!', 'success')
        return redirect_home()
    action = BASE_HREF + "/study/" + study_id
    title = "Edit Study #" + study_id
    return render_template(
        'form.html',
        form=form,
        action=action,
        title=title,
        description_map={},
        base_href=BASE_HREF
    )


def _get_event_data_string(irb_info):
    event = irb_info.IRBEVENT.first().EVENT
    event_id = irb_info.IRBEVENT.first().EVENT_ID
    event_data_string = "('" + event_id + "', '" + event + "')"
    return event_data_string


def _get_status_data_string(irb_info):
    status = irb_info.IRB_STATUS.first().STATUS
    status_id = irb_info.IRB_STATUS.first().STATUS_ID
    status_data_string = "('" + status_id + "', '" + status + "')"
    return status_data_string


@app.route('/irb_info/<study_id>', methods=['GET', 'POST'])
def edit_irb_info(study_id):
    irb_info = db.session.query(IRBInfo).filter(IRBInfo.SS_STUDY_ID == study_id).first()
    form = IRBInfoForm(request.form, obj=irb_info)
    action = BASE_HREF + "/irb_info/" + study_id
    title = "Edit IRB Info #" + study_id
    if request.method == 'GET' and irb_info:
        if irb_info.IRBEVENT and irb_info.IRBEVENT.first():
            form.IRBEVENT.data = _get_event_data_string(irb_info)
        if irb_info.IRB_STATUS and irb_info.IRB_STATUS.first():
            form.IRB_STATUS.data = _get_status_data_string(irb_info)
        if isinstance(irb_info.UVA_IRB_HSR_IS_IRB_OF_RECORD_FOR_ALL_SITES, int):
            form.UVA_IRB_HSR_IS_IRB_OF_RECORD_FOR_ALL_SITES.data = irb_info.UVA_IRB_HSR_IS_IRB_OF_RECORD_FOR_ALL_SITES
    if request.method == 'POST':
        if form.validate():
            _update_irb_info(study_id, irb_info, form)
            flash('IRB Info updated successfully!', 'success')
            return redirect_home()
    return render_template(
        'form.html',
        form=form,
        action=action,
        title=title,
        description_map={},
        base_href=BASE_HREF
    )


@app.route('/investigator/<study_id>', methods=['GET', 'POST'])
def new_investigator(study_id):
    form = InvestigatorForm(request.form)

    # Remove options from form if unique investigator already exist, but AS_C and SI can happen many times.
    investigators = db.session.query(Investigator).filter(Investigator.STUDYID == study_id).all()
    choices = form.INVESTIGATORTYPE.choices
    existing_types = [i.INVESTIGATORTYPE for i in investigators]
    existing_types = list(filter(lambda a: a != "AS_C", existing_types))
    existing_types = list(filter(lambda a: a != "SI", existing_types))
    new_choices = [choice for choice in choices if choice[0] not in existing_types]
    form.INVESTIGATORTYPE.choices = new_choices

    action = BASE_HREF + "/investigator/" + study_id
    title = "Add Investigator to Study " + study_id
    if request.method == 'POST':
        investigator = Investigator(STUDYID=study_id)
        investigator.NETBADGEID = form.NETBADGEID.data
        investigator.set_type(form.INVESTIGATORTYPE.data)
        db.session.add(investigator)
        db.session.commit()
        flash('Investigator created successfully!', 'success')
        return redirect_home()

    return render_template(
        'form.html',
        form=form,
        action=action,
        title=title,
        description_map={},
        base_href=BASE_HREF
    )


@app.route('/del_investigator/<inv_id>', methods=['GET', 'POST'])
def del_investigator(inv_id):
    inv_id = int(inv_id)
    inv_model = db.session.query(Investigator).filter(Investigator.id == inv_id).first()
    if inv_model is None:
        flash('Investigator not found.', 'warn')
        return redirect_home()

    uid = inv_model.NETBADGEID
    study_id = int(inv_model.STUDYID)
    form = ConfirmDeleteForm(request.form, obj=inv_model)

    if request.method == 'GET':
        action = BASE_HREF + "/del_investigator/%i" % inv_id
        title = "Delete Investigator #%i?" % inv_id
        details = "Are you sure you want to delete Investigator '%s' from Study %i?" % (uid, study_id)

        return render_template(
            'form.html',
            form=form,
            action=action,
            title=title,
            details=details,
            description_map=description_map,
            base_href=BASE_HREF
        )

    if request.method == 'POST':
        if form.confirm and form.confirm.data:
            db.session.query(Investigator).filter(Investigator.id == inv_id).delete()
            db.session.commit()
            flash('Investigator %s deleted from Study %i.' % (uid, study_id), 'success')
        else:
            flash('Delete canceled.', 'info')

    return redirect_home()


@app.route('/study_sponsor/<study_id>', methods=['GET', 'POST'])
def edit_study_sponsor(study_id):
    study = db.session.query(Study).filter(Study.STUDYID == study_id).first()
    form = StudySponsorForm(request.form)
    action = BASE_HREF + "/study_sponsor/" + study_id
    title = "Edit sponsors for Study " + study_id
    form.SPONSOR_IDS.choices = [(s.SPONSOR_ID, f'{s.SP_NAME} ({s.SP_TYPE})') for s in db.session.query(Sponsor).all()]

    if request.method == 'GET':
        if hasattr(study, 'sponsors'):
            form.SPONSOR_IDS.data = [s.SPONSOR_ID for s in study.sponsors]

    if request.method == 'POST':
        # Remove all existing sponsors
        session.query(StudySponsor).filter(StudySponsor.SS_STUDY == study_id).delete()

        # Add the new ones
        for sponsor_id in form.SPONSOR_IDS.data:
            study_sponsor = StudySponsor(SS_STUDY=study_id, SPONSOR_ID=sponsor_id)
            db.session.add(study_sponsor)
            db.session.commit()

        sponsor_label = 'sponsor' if len(form.SPONSOR_IDS.data) == 1 else 'sponsors'
        flash(f'Study {sponsor_label} edited successfully!', 'success')
        return redirect_home()

    return render_template(
        'form.html',
        form=form,
        action=action,
        title=title,
        description_map={},
        base_href=BASE_HREF
    )


@app.route('/del_study_sponsor/<study_sponsor_id>', methods=['GET', 'POST'])
def del_study_sponsor(study_sponsor_id):
    study_sponsor_id = int(study_sponsor_id)
    study_sponsor_model: StudySponsor = db.session.query(StudySponsor).filter(
        StudySponsor.id == study_sponsor_id).first()

    if study_sponsor_model is None:
        flash('StudySponsor not found.', 'warn')
        return redirect_home()

    sponsor_span = f'<span class="highlight">{study_sponsor_model.sponsor.SP_NAME} ' \
                   f'({study_sponsor_model.sponsor.SP_TYPE})</span>'
    study_id = int(study_sponsor_model.SS_STUDY)
    form = ConfirmDeleteForm(request.form, obj=study_sponsor_model)

    if request.method == 'GET':
        action = f'{BASE_HREF}/del_study_sponsor/{study_sponsor_id}'
        title = 'Remove study sponsor?'
        details = f'Are you sure you want to remove {sponsor_span} ' \
                  f'as a sponsor of Study {study_id}? ' \
                  f'This will not remove the sponsor itself from the system.'

        return render_template(
            'form.html',
            form=form,
            action=action,
            title=title,
            details=details,
            description_map=description_map,
            base_href=BASE_HREF
        )

    if request.method == 'POST':
        if form.confirm and form.confirm.data:
            db.session.query(StudySponsor).filter(StudySponsor.id == study_sponsor_id).delete()
            db.session.commit()
            flash(f'Sponsor {sponsor_span} removed from Study {study_id}.', 'success')
        else:
            flash('Delete canceled.', 'info')

    return redirect_home()


@app.route('/del_study/<study_id>', methods=['GET', 'POST'])
def del_study(study_id):
    study_id = int(study_id)
    study_model = db.session.query(Study).filter(Study.STUDYID == study_id).first()
    if study_model is None:
        flash('Study not found.', 'warn')
        return redirect_home()

    form = ConfirmDeleteForm(request.form, obj=study_model)

    if request.method == 'GET':
        action = f'{BASE_HREF}/del_study/{study_id}'
        title = f'Delete Study #{study_id}?'
        details = f'Are you sure you want to delete Study <span class="highlight">{study_model.TITLE}</span>?'

        return render_template(
            'form.html',
            form=form,
            action=action,
            title=title,
            details=details,
            description_map=description_map,
            base_href=BASE_HREF
        )

    if request.method == 'POST':
        if form.confirm and form.confirm.data:
            db.session.query(RequiredDocument).filter(RequiredDocument.STUDYID == study_id).delete()
            db.session.query(Investigator).filter(Investigator.STUDYID == study_id).delete()
            db.session.query(StudyDetails).filter(StudyDetails.STUDYID == study_id).delete()
            db.session.query(StudySponsor).filter(StudySponsor.SS_STUDY == study_id).delete()
            db.session.query(IRBStatus).filter(IRBStatus.STUDYID == study_id).delete()
            db.session.query(IRBInfoEvent).filter(IRBInfoEvent.STUDY_ID == study_id).delete()
            db.session.query(IRBInfoStatus).filter(IRBInfoStatus.STUDY_ID == study_id).delete()
            db.session.query(IRBInfo).filter(IRBInfo.SS_STUDY_ID == study_id).delete()
            study = db.session.query(Study).filter(Study.STUDYID == study_id).first()
            session.delete(study)
            db.session.commit()
            flash('Study %i deleted.' % study_id, 'success')
        else:
            flash('Delete canceled.', 'info')

        return redirect_home()


def _get_review_type_name(review_type):
    if review_type == '1':
        return ''
    elif review_type == '2':
        return 'Full Committee'
    elif review_type == '3':
        return 'Expedited'
    elif review_type == '23':
        return 'Non-UVA IRB Full Board'
    elif review_type == '24':
        return 'Non-UVA IRB Expedited'


@app.route('/study_details/<study_id>', methods=['GET', 'POST'])
def study_details(study_id):
    study_details = db.session.query(StudyDetails).filter(StudyDetails.STUDYID == study_id).first()
    if not study_details:
        study_details = StudyDetails(STUDYID=study_id)
    form = StudyDetailsForm(request.form, obj=study_details)

    action = url_for("study_details", study_id=study_id)
    title = "Edit Study Details for Study #" + study_id
    details = "Numeric fields can be 1 for true, 0 or false, or Null if not applicable."

    if request.method == 'POST':
        # update study details with csv file
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                flash('No file selected', 'failure')
                return redirect(action)
            elif file and _allowed_file(file.filename):
                process_csv_study_details(study_id, file)
                flash('CSV file uploaded', 'success')
                return redirect_home()
            else:
                flash('There was a problem processing your file', 'failure')
                return redirect(action)

        # update study details from the form
        elif form.validate():
            if form.REVIEW_TYPE.data:
                REVIEWTYPENAME = _get_review_type_name(form.REVIEW_TYPE.data)
                study_details.REVIEWTYPENAME = REVIEWTYPENAME
            form.populate_obj(study_details)
            db.session.add(study_details)
            db.session.commit()
            flash('Study updated successfully!', 'success')
            return redirect_home()

    # display the study details form
    return render_template(
        'form.html',
        form=form,
        action=action,
        csv_action=action,
        title=title,
        details=details,
        description_map=description_map,
        base_href=BASE_HREF
    )


# from pb.ldap_service import users_as_json
@app.route('/search_ldap/<needle>')
def search_ldap(needle):
    return LdapService.users_as_json(needle)


@app.route('/site_map')
def site_map():
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = app.confg['APPLICATION_ROOT'].strip('/') + url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    return json.dumps({"links": links})


@app.route('/verify_document_list', methods=['GET'])
def verify_document_list():
    verify = verify_required_document_list()
    if verify:
        flash('Document list is up to date.', 'success')
    else:
        flash('The document list is not up to date.', 'failure')

    return redirect_home()


@app.route('/verify_study_details')
def verify_study_details():
    verify = verify_study_details_list()
    if verify:
        flash('Study details are up to date.', 'success')
    else:
        flash('Study details are not up to date.', 'failure')
    return redirect_home()
