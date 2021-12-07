from pb import session
from pb.models import Investigator, InvestigatorSchema, IRBInfo, IRBInfoSchema, \
                      IRBStatus, IRBStatusSchema, RequiredDocument, RequiredDocumentSchema, \
                      Study, StudySchema, StudyDetails, StudyDetailsSchema, \
                      StudySponsor, StudySponsorSchema, CreatorStudySchema


def get_user_studies(uva_id):
    studies = session.query(Study).filter(Study.NETBADGEID == uva_id).all()
    return CreatorStudySchema(many=True).dump(studies)


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
    return IRBInfoSchema().dump(irb_info)
