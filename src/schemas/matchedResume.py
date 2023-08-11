from pydantic import BaseModel, EmailStr


class ResumeMatchedModel(BaseModel):
    id: int = Field(default=None, alias="id")
    id_resume : int = Field()
    job_index : int = Field()
    degrees_matching : float = Field()
    job_title_matching : float = Field()
    skills_matching :float = Field()
    experiences_matching : float = Field()

    
    class Config:
        allow_population_by_field_name = True