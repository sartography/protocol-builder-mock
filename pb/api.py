from pb import session
from pb.models import Investigator, InvestigatorSchema, IRBInfo, IRBInfoSchema, IRBInfoErrorSchema,\
                      IRBStatus, IRBStatusSchema, RequiredDocument, RequiredDocumentSchema, \
                      Study, StudySchema, StudyDetails, StudyDetailsSchema, \
                      StudySponsor, StudySponsorSchema, CreatorStudySchema, \
                      PreReview, PreReviewSchema, PreReviewErrorSchema


def get_user_studies(uva_id):
    non_exempt_studies = []
    exempt_studies = []
    studies = (session.query(Study).filter(Study.NETBADGEID == uva_id).all())
    for study in studies:
        irb_info = study.irb_info.first()
        if hasattr(irb_info, 'IRB_REVIEW_TYPE'):
            if irb_info.IRB_REVIEW_TYPE != 'Exempt':
                non_exempt_studies.append(study)
            else:
                exempt_studies.append(study)
        else:
            non_exempt_studies.append(study)
    return CreatorStudySchema(many=True).dump(non_exempt_studies)


def required_docs(studyid):
    docs = session.query(RequiredDocument).filter(RequiredDocument.STUDYID == studyid).all()
    docs_schema = RequiredDocumentSchema(many=True).dump(docs)
    return {'AUXDOCS': docs_schema,
            'TEMPLATEDOCS': [],
            'OTHERDOCS': []}


def investigators(studyid):
    inv = session.query(Investigator).filter(Investigator.STUDYID == studyid).all()
    return InvestigatorSchema(many=True).dump(inv)


def sponsors(studyid):
    sponsors = session.query(StudySponsor).filter(StudySponsor.SS_STUDY == studyid).all()
    return StudySponsorSchema(many=True).dump(sponsors)


def get_study_details(studyid):
    details = session.query(StudyDetails).filter(StudyDetails.STUDYID == studyid).first()
    return [StudyDetailsSchema().dump(details)]


def check_study(studyid):
    irb_status = session.query(IRBStatus).filter(IRBStatus.STUDYID == studyid).first()
    return IRBStatusSchema().dump(irb_status)


def current_irb_info(studyid):
    irb_info = session.query(IRBInfo).filter(IRBInfo.SS_STUDY_ID == studyid).first()
    if irb_info and hasattr(irb_info, 'IRB_ONLINE_STATUS') and irb_info.IRB_ONLINE_STATUS == 'Error':
        # IRB Online returns a dictionary in this case
        return IRBInfoErrorSchema().dump(irb_info)
    else:
        # IRB Online returns a list with 1 dictionary in this case
        return IRBInfoSchema(many=True).dump([irb_info])


def pre_reviews(study_id):
    results = session.query(PreReview).filter(PreReview.SS_STUDY_ID == study_id).all()
    if results:
        return PreReviewSchema(many=True).dump(results)
    pre_review = PreReview(STATUS='Error', DETAIL='No records found.')
    return PreReviewErrorSchema().dump(pre_review)
