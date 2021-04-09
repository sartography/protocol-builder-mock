from pb import session
from pb.models import Investigator, InvestigatorSchema, IRBStatus, IRBStatusSchema, \
                      RequiredDocument, RequiredDocumentSchema, Study, StudySchema, \
                      StudyDetails, StudyDetailsSchema, StudySponsor, StudySponsorSchema


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
