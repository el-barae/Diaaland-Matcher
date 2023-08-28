from pydantic import BaseModel
from typing import List


class Skill(BaseModel):
    id: int
    name: str
    type_: str

    class Config:
        orm_mode = True


class Experience(BaseModel):
    id: int
    name: str
    candidate_id: int

    class Config:
        orm_mode = True


class Education(BaseModel):
    id: int
    name: str
    diplomat: str
    candidate_id: int

    class Config:
        orm_mode = True


class Job(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        orm_mode = True


class Certificate(BaseModel):
    id: int
    name: str
    id_link_certificate: int

    class Config:
        orm_mode = True


class Candidate(BaseModel):
    id: int
    first_name: str
    last_name: str
    description: str
    skills: List[Skill] = []
    experiences: List[Experience] = []
    certifications: List[Certificate] = []
    degrees: List[Education] = []
    jobs: List[Job] = []

    class Config:
        orm_mode = True


class CandidateJob(BaseModel):
    id: int
    candidate_id: int
    job_id: int

    class Config:
        orm_mode = True


class CandidateSkill(BaseModel):
    id: int
    candidate_id: int
    skill_id: int

    class Config:
        orm_mode = True
