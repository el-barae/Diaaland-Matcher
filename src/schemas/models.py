from sqlalchemy.orm import declarative_base
from sqlalchemy import ForeignKey, String, Column, Integer, Date
from sqlalchemy.orm import relationship

Base = declarative_base()

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    description = Column(String)
    

    skills = relationship("Skills",secondary="candidate_skills")
    jobs = relationship("Jobs", secondary="candidate_jobs")
    experiences = relationship("Experiences", back_populates="candidate")
    certifications = relationship("Certificates", back_populates="candidate")
    degrees = relationship("Educations", back_populates="candidates")


class Jobs(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)


class Candidates_jobs(Base):
    __tablename__ = "candidates_jobs"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey('candidates.id'))
    job_id = Column(Integer, ForeignKey('jobs.id'))


class Skills(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    type_ = Column(String)


class Candidates_skills(Base):
    __tablename__ = "candidate_skills"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey('candidates.id'))
    skill_id = Column(Integer, ForeignKey('skills.id'))
    score = Column(Integer)


class Experiences(Base):
    __tablename__ = "experiences"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    candidate_id = Column(Integer, ForeignKey('candidates.id'))


class Educations(Base):
    __tablename__ = "educations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    diplomat = Column(String)
    candidate_id = Column(Integer, ForeignKey('candidates.id'))


class Certificates(Base):
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    id_link_certificate = Column(Integer, ForeignKey('candidates.id'))