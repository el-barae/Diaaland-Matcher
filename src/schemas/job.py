from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, Field


Base = declarative_base()


# Define SQLAlchemy model for PostgreSQL
class JobDBModel(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)


# Define Pydantic model for API input/output
class JobModel(BaseModel):
    id: int = Field(default=None, alias="id")
    description: str

    class Config:
        population_by_name = True
        from_attributes = True


# session = SessionLocal()

# # Query data from the table
# stmt = select(JobDBModel)
# jobs_data = session.execute(stmt).scalars().all()

# # Close the session
# session.close()

