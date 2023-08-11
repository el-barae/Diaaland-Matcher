from pydantic import BaseModel, Field


# Define Pydantic model for API input/output
class JobModel(BaseModel):
    id: int = Field(default=None, alias="id")
    degrees : list = Field()
    job_title : str = Field()
    skills : list = Field()
    experiences : list = Field()

    class Config:
        allow_population_by_field_name = True
