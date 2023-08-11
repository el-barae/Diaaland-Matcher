from pydantic import BaseModel, EmailStr
from sqlalchemy import Column, Integer, String, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import UUID
import uuid


Base = declarative_base()


class ResumeDBModel(Base):
    __tablename__ = "resumes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    degrees = Column(ARRAY(String))
    job_title = Column(String)
    skills = Column(ARRAY(String))
    experiences = Column(ARRAY(String))


class ResumeModel(BaseModel):
    id: int = Field(default=None, alias="id")
    degrees : list = Field()
    job_title : str = Field()
    skills : list = Field()
    experiences : list = Field()

    class Config:
        allow_population_by_field_name = True
        orm_mode = True


# session = SessionLocal()

# # Query data from the table
# stmt = select(JobDBModel)
# jobs_data = session.execute(stmt).scalars().all()

# # Close the session
# session.close()


