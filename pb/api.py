from pb import session
from pb.models import Investigator, InvestigatorSchema, IRBInfo, IRBInfoSchema, \
                      IRBStatus, IRBStatusSchema, RequiredDocument, RequiredDocumentSchema, \
                      Study, StudySchema, StudyDetails, StudyDetailsSchema, \
                      StudySponsor, StudySponsorSchema, IRBInfoEvent, IRBInfoStatus


def get_user_studies(uva_id):
    studies = session.query(Study).filter(Study.NETBADGEID == uva_id).all()
    return StudySchema(many=True).dump(studies)


def required_docs(studyid):
    docs = session.query(RequiredDocument).filter(RequiredDocument.STUDYID == studyid).all()
    return RequiredDocumentSchema(many=True).dump(docs)


def investigators(studyid):
    inv = session.query(Investigator).filter(Investigator.STUDYID == studyid).all()
    return InvestigatorSchema(many=True).dump(inv)


def sponsors(studyid):
    sponsors = session.query(StudySponsor).filter(StudySponsor.SS_STUDY == studyid).all()
    return StudySponsorSchema(many=True).dump(sponsors)


def get_study_details(studyid):
    details = session.query(StudyDetails).filter(StudyDetails.STUDYID == studyid).first()
    return StudyDetailsSchema().dump(details)


def check_study(studyid):
    irb_status = session.query(IRBStatus).filter(IRBStatus.STUDYID == studyid).first()
    return IRBStatusSchema().dump(irb_status)


def current_irb_info(studyid):
    irb_info = session.query(IRBInfo).filter(IRBInfo.SS_STUDY_ID == studyid).first()
    # new_info = IRBInfo(SS_STUDY_ID=irb_info.SS_STUDY_ID)
    # new_info.UVA_STUDY_TRACKING = irb_info.UVA_STUDY_TRACKING
    # new_info.DATE_MODIFIED = irb_info.DATE_MODIFIED
    # new_info.IRB_ADMINISTRATIVE_REVIEWER = irb_info.IRB_ADMINISTRATIVE_REVIEWER
    # new_info.AGENDA_DATE = irb_info.AGENDA_DATE
    # new_info.IRB_REVIEW_TYPE = irb_info.IRB_REVIEW_TYPE
    # new_info.IRB_OF_RECORD = irb_info.IRB_OF_RECORD
    # new_info.UVA_IRB_HSR_IS_IRB_OF_RECORD_FOR_ALL_SITES = irb_info.UVA_IRB_HSR_IS_IRB_OF_RECORD_FOR_ALL_SITES
    # new_info.STUDYIRBREVIEWERADMIN = irb_info.STUDYIRBREVIEWERADMIN
    # new_info.IRBEVENT = irb_info.IRBEVENT[0]
    # new_info.IRB_STATUS = irb_info.IRB_STATUS[0]
    return IRBInfoSchema().dump(irb_info)
