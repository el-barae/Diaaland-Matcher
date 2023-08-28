from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import ForeignKey, String, Column, Integer, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import quote_ident


class Candidate(DeclarativeBase):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    description = Column(String)
    

    skills = relationship(secondary="candidate_skills")
    experiences = relationship("Experiences", back_populates="candidate")
    certifications = relationship("Certificates", back_populates="candidate")
    degrees = relationship("Educations", back_populates="candidates")
    jobs = relationship(secondary="candidate_jobs")


class Jobs(DeclarativeBase):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)


class Candidates_jobs(DeclarativeBase):
    __tablename__ = "candidates_jobs"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey('candidates.id'))
    job_id = Column(Integer, ForeignKey('jobs.id'))


class Skills(DeclarativeBase):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    type_ = Column(String, name=quote_ident("type"))


class Candidates_skills(DeclarativeBase):
    __tablename__ = "candidate_skills"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey('candidates.id'))
    skill_id = Column(Integer, ForeignKey('skills.id'))
    score = Column(Integer)


class Experiences(DeclarativeBase):
    __tablename__ = "experiences"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    candidate_id = Column(Integer, ForeignKey('candidates.id'))


class Educations(DeclarativeBase):
    __tablename__ = "educations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    diplomat = Column(String)
    candidate_id = Column(Integer, ForeignKey('candidates.id'))


class Certificates(DeclarativeBase):
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    id_link_certificate = Column(Integer, ForeignKey('candidates.id'))